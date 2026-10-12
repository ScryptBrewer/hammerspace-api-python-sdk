"""Local CrewAI chatbot CLI with selectable OpenAI-compatible providers.

Examples:
    python chatbot/bot.py                        # interactive provider picker
    python chatbot/bot.py --provider openai
    python chatbot/bot.py --provider perplexity --model sonar
    python chatbot/bot.py --provider ollama      # fully local, no API key
    python chatbot/bot.py --provider groq --hammerspace
    python chatbot/bot.py --list-providers

API keys are read from the environment or a .env file; see .env.example.
For a Gradio web UI use: python chatbot/app.py
"""
import argparse
import sys

from dotenv import load_dotenv

from backend import ChatService, ProviderError, ConfigError
from providers import PROVIDERS, resolve_api_key

load_dotenv()


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


def _pick_provider() -> str:
    _print_providers()
    choice = input(f"Select provider [{'|'.join(sorted(PROVIDERS))}]: ").strip()
    if choice not in PROVIDERS:
        raise SystemExit(f"Unknown provider '{choice}'")
    return choice


def main() -> None:
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

    provider = args.provider or _pick_provider()
    try:
        service = ChatService(
            provider_name=provider,
            model=args.model,
            temperature=args.temperature,
            read_only=args.read_only,
        )
    except ImportError:
        raise SystemExit(
            "crewai is not installed. Run: pip install -r chatbot/requirements.txt "
            "(Python 3.10-3.12 recommended)"
        )
    except (ProviderError, ConfigError) as exc:
        raise SystemExit(str(exc))

    if service.tools and not args.read_only:
        print(
            "WARNING: cluster management mode - the assistant can create, "
            "update and delete cluster objects. Destructive operations always "
            "require explicit confirmation."
        )
    tools_note = f" | tools: {', '.join(t.name for t in service.tools)}" if service.tools else ""
    print(
        f"Gratto bot ready | provider: {service.provider.name} | "
        f"model: {service.model}{tools_note}"
    )
    print("Type 'quit' or Ctrl-D to exit.\n")

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
            reply = service.chat(user_input)
        except Exception as exc:
            print(f"[error] {exc}\n")
            continue
        print(f"bot> {reply}\n")


if __name__ == "__main__":
    sys.exit(main())
