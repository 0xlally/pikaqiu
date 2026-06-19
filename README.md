# PikaQiu Agent

An LLM-powered autonomous penetration testing agent that runs in a Kali Linux sandbox. It uses a ReAct (Reason + Act) loop to analyze targets, execute commands, and capture flags — all without human intervention.

## How It Works

```
Orchestrator (ReAct Loop)
  ├─ Main Agent (LLM) — analyze context → plan → issue commands
  ├─ Sandbox (Kali Docker) — execute bash/python commands
  ├─ Memory Agent — compress observations into structured memory
  ├─ Passive Observer — periodic runtime audit and corrective steer injection
  ├─ Knowledge Base — offline FTS search (HackTricks, PayloadsAllTheThings, etc.)
  └─ CVE/POC Search — product+version matching with embedded exploits
```

**Key Features:**
- **ReAct loop**: Analyze → Command → Execute → Compress → Repeat
- **Multi-node memory**: Per-IP state tracking, network topology, credential management
- **Auto flag detection**: Scans output for `flag{...}` patterns, multi-flag support
- **Context management**: Importance-graded compression, output truncation, stall detection
- **CVE/POC index**: Product+version matching with embedded PoC code
- **Internet search tools**: `web_search` and `web_fetch` let the agent query public web pages from the sandbox when fresh CVE/PoC data is needed
- **Passive Observer**: Secondary LLM reviews runtime behavior every 16 main-model turns by default; it is not a callable tool
- **Environment auto-discovery**: Sandbox capabilities injected into system prompt

## Quick Start

### Prerequisites

| Component | Requirement |
|-----------|-------------|
| **OS** | Linux (Ubuntu 22.04+), macOS, or Windows with WSL |
| **Docker** | Docker Engine 24.0+ |
| **Python** | 3.11+ |
| **RAM** | ≥ 8GB |
| **Disk** | ≥ 20GB (Kali sandbox image ~6GB) |

### 1. Install dependencies

```bash
git clone https://github.com/0xlally/pikaqiu.git
cd pikaqiu

python -m pip install -r requirements.txt
```

### 2. Configure LLM

Keep the real API key in `.env` so it is not committed:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
PIKAQIU_LLM_BASE_URL=https://www.inroi.shop
PIKAQIU_LLM_MODEL=gpt-5.5
PIKAQIU_LLM_API_KEY=replace-with-your-api-key
PIKAQIU_LLM_REASONING_EFFORT=xhigh
PIKAQIU_LLM_USE_RESPONSES_API=true
PIKAQIU_LLM_DISABLE_RESPONSE_STORAGE=true

PIKAQIU_OBSERVER_BASE_URL=https://www.inroi.shop
PIKAQIU_OBSERVER_MODEL=gpt-5.5
PIKAQIU_OBSERVER_API_KEY=replace-with-your-api-key
PIKAQIU_OBSERVER_REASONING_EFFORT=xhigh
PIKAQIU_OBSERVER_USE_RESPONSES_API=true
PIKAQIU_OBSERVER_DISABLE_RESPONSE_STORAGE=true
PIKAQIU_OBSERVER_REVIEW_INTERVAL=16
```

`config.yml` provides the default model and sandbox settings. Environment variables in `.env` override the main YAML model, so secrets can stay outside tracked files.

Observer is passive: the main agent has no callable supervision tool. The orchestrator invokes the Observer runtime after `observer_review_interval` main-model turns, then injects only actionable audit notes back into the mission context.

### 3. Build and start sandbox

```bash
# If you have sandbox-package.7z/.zip, extract it and run:
#   powershell -ExecutionPolicy Bypass -File .\restore-scripts\restore-sandbox.ps1
# The restore script imports sandbox-rootfs.tar as pikaqiu-kali-sandbox:latest.
#
# Otherwise build Kali sandbox image (~15-30 min first time):
docker build -f Dockerfile.sandbox -t pikaqiu-kali-sandbox .

# Start sandbox container
docker compose up -d

# Verify sandbox command execution
docker exec pikaqiu-sandbox-1 bash -lc "pwd && python3 --version"
```

The agent uses a single sandbox container, `pikaqiu-sandbox-1`, with workdir `/tmp/pikaqiu-agent-workspace`.

### 4. Run Web UI

```bash
python -m pikaqiu_agent
# Open http://127.0.0.1:8001
```

Create a mission via the Web UI or API. This starts active testing against the target:

```bash
curl -X POST http://localhost:8001/api/missions \
  -H "Content-Type: application/json" \
  -d '{"name":"pikaqiu-target","target":"http://10.50.1.182:36543/","goal":"Find and capture all flags","expected_flags":1}'
```

## Project Structure

```
pikaqiu_agent/
  ├─ orchestrator.py   # ReAct main loop, mission execution
  ├─ llm_client.py     # LangChain LLM wrapper (model pool, failover)
  ├─ prompts.py        # System prompts and context building
  ├─ tools.py          # Tool definitions (bash, python, web, flag submission)
  ├─ sandbox.py        # Docker sandbox command execution
  ├─ memory.py         # Memory compression (multi-node, topology)
  ├─ knowledge.py      # Knowledge base indexer (FTS + CVE)
  ├─ storage.py        # SQLite persistence
  ├─ config.py         # Configuration (YAML + runtime adjustable)
  ├─ web_app.py        # Flask Web backend
  └─ static/           # Frontend
      ├─ index.html    # Mission dashboard
      └─ settings.html # Settings page

config.yml             # Main configuration
skills/                # Mission skills using one SKILL.md file per skill
Dockerfile.sandbox     # Kali sandbox image
docker-compose.yml     # Container orchestration
requirements.txt       # Python dependencies
```

## Knowledge Base

Place knowledge files under the configured `knowledge_dir` (default: `./knowledge/`).

Supported formats:
- **ZIP archives** — automatically extracted and indexed (e.g., `hacktricks.zip`, `PayloadsAllTheThings.zip`)
- **Directories** — recursively indexed

### CVE/POC Index

Place a `cve-poc-index.json` file in `knowledge_dir` for structured CVE search:
- Product name matching: `search_cve(product="thinkphp")`
- Version range matching: `search_cve(product="redis", version="5.0.5")`
- Vulnerability type filter: `search_cve(vuln_type="deserialization")`
- CVE ID lookup: `search_cve(cve_id="CVE-2021-44228")`

## Skills

Place skills under the configured `skills_dir` (default: `./skills/`).
Each skill lives in its own folder and uses a single `SKILL.md` file with YAML frontmatter plus a Markdown body. The built-in layout is `skills/builtin/<skill-name>/SKILL.md`.

Example:

```text
skills/
  builtin/
    recon/
      SKILL.md
    ffuf-skill/
      SKILL.md
```

`SKILL.md` format:

```markdown
---
name: recon
description: Use for new targets, attack-surface discovery, service mapping, and initial web reconnaissance.
tags: [web, recon]
enabled: true
---

# Recon

Follow the reconnaissance workflow here.
```

List loaded skills:

```bash
curl http://localhost:8001/api/skills
```

Enable skills when creating a mission:

```bash
curl -X POST http://localhost:8001/api/missions \
  -H "Content-Type: application/json" \
  -d '{"name":"pikaqiu-target","target":"http://10.50.1.182:36543/","goal":"Find and capture all flags","expected_flags":1,"skills":["recon"]}'
```

The AI can also activate skills automatically during a mission when `skills_auto_use` is enabled:

- `skill_search`: searches loaded `SKILL.md` metadata for the current situation.
- `activate_skill`: loads one relevant skill body and records it in the mission.
- `skill_read_reference`: reads optional files bundled inside a skill only when needed.

`knowledge/` is searchable reference material used by `knowledge_search`.
Manually selected skills and AI-activated skills are injected into later rounds.

## Sandbox Tools

The Kali Docker sandbox is built from the official `kalilinux/kali-rolling` image and installs a practical baseline toolset:

- **Network**: nmap, netcat, socat, curl, wget, dig, whois
- **Web**: sqlmap and Python HTTP tooling
- **Runtimes**: Python 3, Python 2.7, Node.js, Java 8/17, PHP, Perl
- **Python packages**: requests/httpx/aiohttp, PyJWT, flask-unsign, impacket, certipy-ad, bloodyAD
- **Browser automation**: Playwright with Chromium
- **Project tools**: `/opt/pikaqiu-tools/env-info` for runtime capability discovery

## Configuration Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `initial_rounds` | 8 | Max reasoning rounds per mission |
| `initial_commands` | 200 | Max tool calls per round |
| `command_timeout_sec` | 300 | Single command timeout |
| `llm_timeout_sec` | 240 | LLM API call timeout |
| `stdout_limit` | 8000 | Output truncation threshold (chars) |
| `knowledge_top_k` | 6 | Knowledge search results count |
| `knowledge_dir` | `./knowledge` | Path to knowledge base files |
| `skills_dir` | `./skills` | Path to skill folders containing `SKILL.md` |
| `skills_auto_use` | `true` | Allow the AI to search and activate skills during a mission |
| `skill_catalog_limit` | `50` | Max skill metadata entries injected into the system prompt |
| `skill_prompt_max_chars` | `12000` | Max `SKILL.md` body chars returned by `activate_skill` |
| `skill_reference_max_chars` | `20000` | Max chars returned by `skill_read_reference` |

## License
