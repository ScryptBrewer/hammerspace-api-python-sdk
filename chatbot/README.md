# Gratto Bot — local CrewAI chatbot

A local chatbot built on the [CrewAI](https://github.com/crewAIInc/crewAI)
framework. Every provider is reached through the OpenAI-compatible
chat-completions API, so you can point the same bot at OpenAI, Perplexity,
Groq, Ollama (fully local), or any other OpenAI-style endpoint just by
choosing where the API token comes from.

## Setup

```bash
python3.11 -m venv .venv-chatbot          # CrewAI supports Python 3.10-3.12
source .venv-chatbot/bin/activate
pip install -r chatbot/requirements.txt
pip install -e .                          # only needed for --hammerspace tools

cp chatbot/.env.example .env              # then fill in one API key
```

## Choose a provider (API token target)

| Provider   | Env key             | Default model | Notes                          |
|------------|---------------------|---------------|--------------------------------|
| openai     | `OPENAI_API_KEY`    | gpt-4o-mini   | GPT models                     |
| perplexity | `PERPLEXITY_API_KEY`| sonar-pro     | online models with web search  |
| groq       | `GROQ_API_KEY`      | llama-3.3-70b | very fast open models          |
| together   | `TOGETHER_API_KEY`  | Llama-3.3-70B | open-model hosting             |
| mistral    | `MISTRAL_API_KEY`   | mistral-large | Mistral models                 |
| deepseek   | `DEEPSEEK_API_KEY`  | deepseek-chat | V3/R1                          |
| openrouter | `OPENROUTER_API_KEY`| openai/gpt-4o-mini | gateway to many models    |
| ollama     | —                   | llama3.2      | fully local, no key needed     |
| custom     | `CUSTOM_LLM_*`      | —             | any OpenAI-compatible endpoint |

## Run

```bash
python chatbot/bot.py                          # interactive provider picker
python chatbot/bot.py --provider openai
python chatbot/bot.py --provider perplexity --model sonar
python chatbot/bot.py --provider ollama        # 100% local, no API key
python chatbot/bot.py --list-providers         # show providers + key status
```

## Hammerspace cluster management (optional)

Give the bot full lifecycle control of a live appliance:

```bash
# in .env
HS_BASE_URL=https://your-appliance
HS_USERNAME=admin
HS_PASSWORD=...

python chatbot/bot.py --provider groq --hammerspace             # full management
python chatbot/bot.py --provider groq --hammerspace --read-only # inspection only
```

29 tools across 10 read-only + 19 management operations:

- **Shares**: create, update, delete, move; list/get
- **Objectives (SLAs)**: create, delete; list
- **Storage volumes**: add, remove; list
- **Volume groups**: create, delete; list
- **Users**: create, delete, set password; list
- **Sites (global namespace)**: add remote site, remove site; list
- **Snapshots**: create, restore, delete; list per share
- **Cluster**: system info, nodes, tasks (check completion after writes)
- **`api_call`**: escape hatch to *any* of the 373 generated SDK operations
  (licenses, network, DNS, NTP, KMS, IdP, syslog, software update, …)

### Safety guardrails

- Every destructive operation (delete/restore/move/site pairing) refuses to
  run unless the tool is called with `confirm=true` — the assistant is
  instructed to ask you in chat first.
- `--read-only` strips all write tools entirely.
- After each write the assistant checks the cluster task result via
  `get_tasks`.

Example session:

```
you> create a share called project-files at /exports/project-files, LAN objective, RW for subnet 10.0.0.0/24
bot> [creates the share, reports the task result]
you> now delete it
bot> That will delete the share "project-files". Confirm?
you> yes
bot> [re-calls delete with confirm=true, reports completion]
```
