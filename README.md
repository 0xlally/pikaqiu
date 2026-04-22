# PikaQiu Agent

An LLM-powered autonomous penetration testing agent that runs in a Kali Linux sandbox. It uses a ReAct (Reason + Act) loop to analyze targets, execute commands, and capture flags — all without human intervention.

## How It Works

```
Orchestrator (ReAct Loop)
  ├─ Main Agent (LLM) — analyze context → plan → issue commands
  ├─ Sandbox (Kali Docker) — execute bash/python commands
  ├─ Memory Agent — compress observations into structured memory
  ├─ Advisor Agent — expert consultation when stuck
  ├─ Knowledge Base — offline FTS search (HackTricks, PayloadsAllTheThings, etc.)
  └─ CVE/POC Search — product+version matching with embedded exploits
```

**Key Features:**
- **ReAct loop**: Analyze → Command → Execute → Compress → Repeat
- **Multi-node memory**: Per-IP state tracking, network topology, credential management
- **Auto flag detection**: Scans output for `flag{...}` patterns, multi-flag support
- **Context management**: Importance-graded compression, output truncation, stall detection
- **CVE/POC index**: Product+version matching with embedded PoC code
- **Advisor tool**: Secondary LLM provides expert guidance when the agent is stuck
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
PIKAQIU_LLM_BASE_URL=http://10.50.1.215:8080/v1
PIKAQIU_LLM_MODEL=minimax-m2.7
PIKAQIU_LLM_API_KEY=replace-with-your-api-key
```

`config.yml` provides the default model and sandbox settings. Environment variables in `.env` override the main YAML model, so secrets can stay outside tracked files.

### 3. Build and start sandbox

```bash
# Build Kali sandbox image (~15-30 min first time)
docker build -f Dockerfile.sandbox -t pikaqiu-kali-sandbox .

# Start sandbox containers
docker compose up -d
```

The default active sandbox is `pikaqiu-sandbox-1`, with workdir `/tmp/pikaqiu-agent-workspace`.

### 4. Run Web UI

```bash
python -m pikaqiu_agent
# Open http://127.0.0.1:8765
```

Create a mission via the Web UI or API. This starts active testing against the target:

```bash
curl -X POST http://localhost:8765/api/missions \
  -H "Content-Type: application/json" \
  -d '{"name":"pikaqiu-target","target":"http://10.50.1.182:36543/","goal":"Find and capture all flags","expected_flags":1}'
```

## Project Structure

```
pikaqiu_agent/
  ├─ orchestrator.py   # ReAct main loop, mission execution
  ├─ llm_client.py     # LangChain LLM wrapper (model pool, failover)
  ├─ prompts.py        # System prompts and context building
  ├─ tools.py          # Tool definitions (bash, python, knowledge, CVE, advisor)
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
| `command_timeout_sec` | 60 | Single command timeout |
| `llm_timeout_sec` | 240 | LLM API call timeout |
| `stdout_limit` | 8000 | Output truncation threshold (chars) |
| `knowledge_top_k` | 6 | Knowledge search results count |
| `knowledge_dir` | `./knowledge` | Path to knowledge base files |

## License

MIT
