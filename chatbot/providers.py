"""Provider registry for the CrewAI chatbot.

Every provider is reached through the OpenAI-compatible chat-completions API
(``openai/<model>`` via LiteLLM), so adding a target is just a base URL plus an
API-key environment variable.
"""
import os
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Provider:
    name: str
    default_model: str
    env_keys: Tuple[str, ...] = ()
    base_url: Optional[str] = None
    requires_key: bool = True
    note: str = ""


PROVIDERS = {
    "openai": Provider(
        name="openai",
        default_model="gpt-4o-mini",
        env_keys=("OPENAI_API_KEY",),
        note="GPT models; key from platform.openai.com",
    ),
    "perplexity": Provider(
        name="perplexity",
        default_model="sonar-pro",
        env_keys=("PERPLEXITY_API_KEY",),
        base_url="https://api.perplexity.ai",
        note="Online models with web search; key from perplexity.ai",
    ),
    "groq": Provider(
        name="groq",
        default_model="llama-3.3-70b-versatile",
        env_keys=("GROQ_API_KEY",),
        base_url="https://api.groq.com/openai/v1",
        note="Fast Llama/Mixtral inference; key from console.groq.com",
    ),
    "together": Provider(
        name="together",
        default_model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        env_keys=("TOGETHER_API_KEY",),
        base_url="https://api.together.xyz/v1",
        note="Open-model hosting; key from api.together.xyz",
    ),
    "mistral": Provider(
        name="mistral",
        default_model="mistral-large-latest",
        env_keys=("MISTRAL_API_KEY",),
        base_url="https://api.mistral.ai/v1",
        note="Mistral models; key from console.mistral.ai",
    ),
    "deepseek": Provider(
        name="deepseek",
        default_model="deepseek-chat",
        env_keys=("DEEPSEEK_API_KEY",),
        base_url="https://api.deepseek.com/v1",
        note="DeepSeek V3/R1; key from platform.deepseek.com",
    ),
    "openrouter": Provider(
        name="openrouter",
        default_model="openai/gpt-4o-mini",
        env_keys=("OPENROUTER_API_KEY",),
        base_url="https://openrouter.ai/api/v1",
        note="Gateway to hundreds of models; key from openrouter.ai",
    ),
    "ollama": Provider(
        name="ollama",
        default_model="llama3.2",
        env_keys=(),
        base_url="http://localhost:11434/v1",
        requires_key=False,
        note="Fully local, no API key; requires Ollama running (ollama pull llama3.2)",
    ),
    "custom": Provider(
        name="custom",
        default_model="",
        env_keys=("CUSTOM_LLM_API_KEY",),
        base_url=None,
        note=(
            "Any OpenAI-compatible endpoint: set CUSTOM_LLM_BASE_URL, "
            "CUSTOM_LLM_API_KEY, CUSTOM_LLM_MODEL"
        ),
    ),
}


def resolve_api_key(provider: Provider) -> Optional[str]:
    """Pick the first set env var for the provider, falling back to a shared key."""
    for key in provider.env_keys:
        value = os.getenv(key)
        if value:
            return value
    return os.getenv("LLM_API_KEY")


def resolve_base_url(provider: Provider) -> Optional[str]:
    if provider.name == "custom":
        return os.getenv("CUSTOM_LLM_BASE_URL")
    return provider.base_url


def resolve_model(provider: Provider, model_override: Optional[str] = None) -> str:
    if model_override:
        return model_override
    if provider.name == "custom":
        return os.getenv("CUSTOM_LLM_MODEL", "")
    return provider.default_model
