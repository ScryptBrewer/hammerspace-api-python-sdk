"""Gratto chat GUI — Gradio frontend over the ChatService backend.

Run:  python chatbot/app.py   then open http://127.0.0.1:7860
"""
from __future__ import annotations

import os
import sys

import gradio as gr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import ChatService  # noqa: E402
from providers import PROVIDERS, resolve_api_key  # noqa: E402

THEME_CSS = """
:root {
  --brand-gold: #ecad0a;
  --brand-blue: #209dd7;
  --brand-purple: #753991;
  --bg-soft: #f7f7f9;
  --bg-panel: #ffffff;
  --border: rgba(128, 128, 128, 0.22);
  --text-muted: #5f6470;
}

.dark :root, .dark {
  --bg-soft: #111318;
  --bg-panel: #171a21;
  --border: rgba(255, 255, 255, 0.12);
  --text-muted: #a8b0bd;
}

.gradio-container {
  background: linear-gradient(180deg, var(--bg-soft) 0%, var(--bg-panel) 100%);
}

.app-shell {
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px;
  background: var(--bg-panel);
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.hero {
  border-radius: 18px;
  padding: 22px;
  color: white;
  background: linear-gradient(135deg, #209dd7 0%, #753991 60%, #ecad0a 140%);
}

.hero h1, .hero p { margin: 0; }

.small-note { color: var(--text-muted); font-size: 0.95rem; }

.gr-button.primary {
  background: linear-gradient(135deg, var(--brand-blue), var(--brand-purple));
  color: white;
  border: none;
}
.gr-button.secondary { border-color: var(--brand-gold); }
"""

service: ChatService | None = None


def _default_provider() -> str:
    for name in sorted(PROVIDERS):
        if PROVIDERS[name].requires_key and resolve_api_key(PROVIDERS[name]):
            return name
    return "ollama" if "ollama" in PROVIDERS else sorted(PROVIDERS)[0]


def _describe(service_obj: ChatService | None) -> str:
    if service_obj is None:
        return "Assistant not started — pick a provider and press **Start assistant**."
    return (
        f"**{service_obj.provider.name}** | model: `{service_obj.model}` | "
        f"mode: {service_obj.mode} | tools: {len(service_obj.tools)} | "
        f"turns in memory: {len(service_obj.history)}"
    )


def ui_start(provider: str, model: str, api_key: str, temperature: float,
             hs_base_url: str, hs_username: str, hs_password: str, read_only: bool):
    """Build (or rebuild) the ChatService from the settings tab."""
    global service
    try:
        if api_key:
            for env_key in PROVIDERS[provider].env_keys:
                os.environ[env_key] = api_key
        service = ChatService(
            provider_name=provider,
            model=model or None,
            temperature=temperature,
            hs_base_url=hs_base_url,
            hs_username=hs_username,
            hs_password=hs_password,
            read_only=read_only,
        )
        warning = (
            "\n\n⚠️ **Cluster management mode** — the assistant can modify the "
            "cluster. Destructive operations always require explicit confirmation."
            if service.tools and not read_only else ""
        )
        return (f"✅ Assistant ready — {_describe(service)}{warning}", _describe(service))
    except Exception as exc:
        service = None
        return (f"❌ {exc}", _describe(None))


def ui_respond(message: str, history: list):
    """One chat turn: append the user message, then the assistant reply."""
    history = history or []
    if not message.strip():
        return history, "", _describe(service)
    if service is None:
        history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content":
                "❌ Assistant not started. Open **Settings**, pick a provider, "
                "and press **Start assistant**."},
        ]
        return history, "", _describe(None)
    history = history + [{"role": "user", "content": message}]
    yield history, "", _describe(service)
    try:
        reply = service.chat(message)
    except Exception as exc:
        reply = f"❌ {exc}"
    history = history + [{"role": "assistant", "content": reply}]
    yield history, "", _describe(service)


def ui_clear():
    if service is not None:
        service.reset()
    return [], _describe(service)


with gr.Blocks(title="Gratto — Hammerspace Assistant", css=THEME_CSS) as demo:
    gr.HTML("""
    <div class='hero'>
      <h1>Gratto — Hammerspace Cluster Assistant</h1>
      <p>Chat with your Hammerspace appliance: inspect, create, update, and manage
      shares, SLA objectives, volumes, users, sites, and snapshots — powered by
      CrewAI and any OpenAI-compatible provider.</p>
    </div>
    """)
    gr.Markdown("<div class='small-note'>Local CrewAI chatbot with selectable "
                "providers. Destructive cluster operations always require "
                "explicit confirmation in chat.</div>")

    status_header = gr.Markdown(_describe(None))

    with gr.Tab("Chat"):
        with gr.Column(elem_classes=["app-shell"]):
            chatbot = gr.Chatbot(
                label="Gratto",
                height=480,
                editable=True,
            )
            with gr.Row():
                user_box = gr.Textbox(
                    label="Message",
                    placeholder="e.g. list all shares and node health",
                    scale=5,
                    autofocus=True,
                )
                send_button = gr.Button("Send", variant="primary", scale=1)
            with gr.Row():
                clear_button = gr.Button("Clear conversation", variant="secondary")
            user_box.submit(ui_respond, inputs=[user_box, chatbot], outputs=[chatbot, user_box, status_header])
            send_button.click(ui_respond, inputs=[user_box, chatbot], outputs=[chatbot, user_box, status_header])
            clear_button.click(ui_clear, inputs=None, outputs=[chatbot, status_header])

    with gr.Tab("Settings"):
        with gr.Column(elem_classes=["app-shell"]):
            provider_choice = gr.Dropdown(
                choices=sorted(PROVIDERS),
                value=_default_provider(),
                label="Provider (OpenAI-compatible)",
                interactive=True,
            )
            model_box = gr.Textbox(label="Model (blank = provider default)")
            api_key_box = gr.Textbox(
                label="API key (blank = use environment / .env)",
                type="password",
            )
            temperature_slider = gr.Slider(0.0, 1.5, value=0.7, step=0.1,
                                           label="Temperature")
            gr.Markdown("**Hammerspace connection** (leave base URL empty to chat "
                        "without cluster tools)")
            hs_url_box = gr.Textbox(
                label="Appliance base URL",
                placeholder="https://your-appliance",
            )
            with gr.Row():
                hs_user_box = gr.Textbox(label="Username")
                hs_pass_box = gr.Textbox(label="Password", type="password")
            read_only_check = gr.Checkbox(
                value=False,
                label="Read-only mode (inspection tools only, no writes)",
            )
            start_button = gr.Button("Start assistant", variant="primary")
            start_status = gr.Markdown()
            start_button.click(
                ui_start,
                inputs=[provider_choice, model_box, api_key_box, temperature_slider,
                        hs_url_box, hs_user_box, hs_pass_box, read_only_check],
                outputs=[start_status, status_header],
            )

    gr.Markdown("<div class='small-note'>Tip: after any create/update/delete, "
                "ask the assistant to check task status — it uses get_tasks "
                "automatically.</div>")


if __name__ == "__main__":
    demo.launch()
