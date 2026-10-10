"""Local CrewAI chatbot with selectable OpenAI-compatible providers.

Examples:
    python chatbot/bot.py                        # interactive provider picker
    python chatbot/bot.py --provider openai
    python chatbot/bot.py --provider perplexity --model sonar
    python chatbot/bot.py --provider ollama      # fully local, no API key
    python chatbot/bot.py --provider groq --hammerspace
    python chatbot/bot.py --list-providers

API keys are read from the environment or a .env file; see .env.example.
"""
import argparse
import sys
from typing import List, Optional

from dotenv import load_dotenv

from providers import PROVIDERS, Provider, resolve_api_key, resolve_base_url, resolve_model
from tools import build_tools

HISTORY_TURNS = 12


def _build_llm(provider: Provider, model: Optional[str], temperature: float):
    from crewai import LLM

    api_key = resolve_api_key(provider)
    base_url = resolve_base_url(provider)
    model_name = resolve_model(provider, model)
    if provider.requires_key and not api_key:
        keys = ", ".join(provider.env_keys) or "LLM_API_KEY"
        raise SystemExit(
            f"No API key for provider '{provider.name}'. "
            f"Set one of: {keys} (env or .env file)."
        )
    if not model_name:
        raise SystemExit(
            "No model configured for the custom provider. Set CUSTOM_LLM_MODEL."
        )
    kwargs = {"temperature": temperature}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    return LLM(model=f"openai/{model_name}", **kwargs)


def _build_agent(llm, tools):
    from crewai import Agent

    management = any(t.name.startswith(("create_", "update_", "delete_", "move_",
                                        "set_", "add_", "restore_", "api_call"))
                     for t in tools)
    if tools and management:
        goal = ("Manage the full lifecycle of the user's Hammerspace cluster "
                "(shares, SLA objectives, storage volumes, volume groups, users, "
                "sites, snapshots) and answer status questions from live data")
        backstory = (
            "You are an expert Hammerspace storage administrator assistant. "
            "Use the tools for all cluster operations. You may create and update "
            "freely when asked, but for any DESTRUCTIVE operation (delete, "
            "restore, move, topology change) you MUST first confirm with the "
            "user in chat, then pass confirm=true. After each write, check the "
            "resulting task with get_tasks. The api_call tool reaches any "
            "operation not covered by a dedicated tool."
        )
    elif tools:
        goal = "Answer questions about the user's Hammerspace cluster from live data"
        backstory = "You are a concise Hammerspace status assistant. Read-only."
    else:
        goal = "Chat naturally with the user"
        backstory = "You are a concise, accurate assistant."
    return Agent(
        role="Hammerspace cluster administrator" if tools else "Helpful local assistant",
        goal=goal,
        backstory=backstory,
        llm=llm,
        tools=tools,
        verbose=False,
        memory=False,
    )


def _run_turn(agent, history: List[tuple], user_input: str) -> str:
    from crewai import Crew, Task

    history_text = "\n".join(
        f"User: {u}\nAssistant: {a}" for u, a in history[-HISTORY_TURNS:]
    )
    prompt = user_input if not history_text else (
        f"Conversation so far:\n{history_text}\n\nUser: {user_input}"
    )
    task = Task(
        description=prompt,
        expected_output="A direct, conversational reply to the user's last message.",
        agent=agent,
    )
    return Crew(agents=[agent], tasks=[task], verbose=False).kickoff().raw


def _print_providers() -> None:
    print("Available providers (all via the OpenAI-compatible API):\n")
    for provider in PROVIDERS.values():
        key = resolve_api_key(provider)
        key_state = (
            "key: set" if key
            else "no key needed" if not provider.requires_key
            else "key: MISSING"
        )
        model_label = provider.default_model or "(CUSTOM_LLM_MODEL)"
        print(f"  {provider.name:<12} model={model_label:<42} {key_state}")
        if provider.note:
            print(f"  {'':<12} {provider.note}")
    print()


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--provider", choices=sorted(PROVIDERS), help="LLM provider")
    parser.add_argument("--model", help="Model name (defaults per provider)")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--hammerspace", action="store_true",
                        help="Enable Hammerspace cluster management tools")
    parser.add_argument("--read-only", action="store_true",
                        help="With --hammerspace: inspection tools only, no writes")
    parser.add_argument("--list-providers", action="store_true")
    args = parser.parse_args()

    if args.list_providers:
        _print_providers()
        return

    provider = PROVIDERS[args.provider or _pick_provider()]

    try:
        llm = _build_llm(provider, args.model, args.temperature)
    except ImportError:
        raise SystemExit(
            "crewai is not installed. Run: pip install -r chatbot/requirements.txt "
            "(Python 3.10-3.12 recommended)"
        )
    tools = build_tools(read_only=args.read_only) if args.hammerspace else []
    agent = _build_agent(llm, tools)

    if tools and not args.read_only:
        print(
            "WARNING: cluster management mode - the assistant can create, "
            "update and delete cluster objects. Destructive operations always "
            "require explicit confirmation."
        )
    tools_note = f" | tools: {', '.join(t.name for t in tools)}" if tools else ""
    print(
        f"Gratto bot ready | provider: {provider.name} | "
        f"model: {resolve_model(provider, args.model)}{tools_note}"
    )
    print("Type 'quit' or Ctrl-D to exit.\n")

    history: List[tuple] = []
    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            break
        try:
            reply = _run_turn(agent, history, user_input)
        except Exception as exc:
            print(f"[error] {exc}\n")
            continue
        history.append((user_input, reply))
        print(f"bot> {reply}\n")


def _pick_provider() -> str:
    _print_providers()
    choice = input(f"Select provider [{'|'.join(sorted(PROVIDERS))}]: ").strip()
    if choice not in PROVIDERS:
        raise SystemExit(f"Unknown provider '{choice}'")
    return choice


if __name__ == "__main__":
    sys.exit(main())
