"""Chat backend service for the Gratto assistant.

Mirrors the sandbox backend.py pattern: a framework-free service class with
a small typed exception hierarchy. The Gradio app (app.py) and the CLI
(bot.py) are thin frontends over ChatService.
"""
from __future__ import annotations

import os
from typing import List, Optional

from dotenv import load_dotenv

from providers import PROVIDERS, Provider, resolve_api_key, resolve_base_url, resolve_model
from tools import build_tools

load_dotenv()

HISTORY_TURNS = 12


class ChatError(Exception):
    """Base error for chat service failures."""


class ProviderError(ChatError):
    """Missing API key or unusable provider configuration."""


class ConfigError(ChatError):
    """Invalid service configuration (model, credentials, tools)."""


def build_llm(provider: Provider, model: Optional[str], temperature: float):
    """Create a CrewAI LLM for an OpenAI-compatible provider."""
    from crewai import LLM

    api_key = resolve_api_key(provider)
    base_url = resolve_base_url(provider)
    model_name = resolve_model(provider, model)
    if provider.requires_key and not api_key:
        keys = ", ".join(provider.env_keys) or "LLM_API_KEY"
        raise ProviderError(
            f"No API key for provider '{provider.name}'. Set one of: {keys} "
            "(env or .env file)."
        )
    if not model_name:
        raise ConfigError(
            "No model configured for the custom provider. Set CUSTOM_LLM_MODEL."
        )
    kwargs = {"temperature": temperature}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    return LLM(model=f"openai/{model_name}", **kwargs)


def build_agent(llm, tools):
    """Create the CrewAI agent with a persona matching the toolset."""
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


class ChatService:
    """Stateful chat backend: provider config -> LLM -> agent -> replies.

    One instance owns one conversation. Rebuild (new provider, credentials,
    or mode) by constructing a fresh instance; call reset() to clear history.
    """

    def __init__(
        self,
        provider_name: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        hs_base_url: str = "",
        hs_username: str = "",
        hs_password: str = "",
        read_only: bool = False,
        max_history_turns: int = HISTORY_TURNS,
    ) -> None:
        if provider_name not in PROVIDERS:
            raise ConfigError(
                f"Unknown provider '{provider_name}'. Known: {sorted(PROVIDERS)}"
            )
        self.provider: Provider = PROVIDERS[provider_name]
        self.model = resolve_model(self.provider, model)
        self.temperature = float(temperature)
        self.read_only = bool(read_only)
        self.max_history_turns = max_history_turns
        self.history: List[tuple] = []

        if hs_base_url:
            os.environ["HS_BASE_URL"] = hs_base_url.strip()
            if hs_username:
                os.environ["HS_USERNAME"] = hs_username
            if hs_password:
                os.environ["HS_PASSWORD"] = hs_password
        self.hammerspace_enabled = bool(hs_base_url) or bool(os.getenv("HS_BASE_URL"))

        import tools as tools_module

        tools_module._client = None  # force re-init if credentials changed
        self.tools = (
            build_tools(read_only=self.read_only) if self.hammerspace_enabled else []
        )
        self.llm = build_llm(self.provider, model, self.temperature)
        self.agent = build_agent(self.llm, self.tools)

    @property
    def mode(self) -> str:
        if not self.tools:
            return "chat only (no cluster tools)"
        return "read-only inspection" if self.read_only else "full cluster management"

    def reset(self) -> None:
        self.history.clear()

    def chat(self, user_input: str) -> str:
        """Run one conversation turn and return the assistant reply."""
        from crewai import Crew, Task

        user_input = (user_input or "").strip()
        if not user_input:
            raise ConfigError("Message is empty")

        history_text = "\n".join(
            f"User: {u}\nAssistant: {a}" for u, a in self.history[-self.max_history_turns:]
        )
        prompt = user_input if not history_text else (
            f"Conversation so far:\n{history_text}\n\nUser: {user_input}"
        )
        task = Task(
            description=prompt,
            expected_output="A direct, conversational reply to the user's last message.",
            agent=self.agent,
        )
        reply = Crew(agents=[self.agent], tasks=[task], verbose=False).kickoff().raw
        self.history.append((user_input, reply))
        return reply
