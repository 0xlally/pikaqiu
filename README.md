# PikaQiu Agent — Tencent Penetration Tool

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

### 1. Clone & Build

```bash
git clone https://github.com/0xlally/pikaqiu.git
cd pikaqiu

# Build Kali sandbox image (~15-30 min first time)
docker build -f Dockerfile.sandbox -t pikaqiu-kali-sandbox .

# Start sandbox container
docker compose up -d

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure

Edit `config.yml`:

```yaml
model_pool:
  - id: main
    base_url: "https://api.deepseek.com"
    api_key: "sk-your-key"
    model: "deepseek-reasoner"
    thinking: true
    priority: 1

advisor:
  base_url: "https://api.openai.com/v1"
  api_key: "sk-your-key"
  model: "gpt-4o"

sandbox:
  container: "tencent-pentest-agent-sandbox"
  workdir: "/tmp/pikaqiu-agent-workspace"

web:
  host: "127.0.0.1"
  port: 8765
```

### 3. Run

```bash
python -m pikaqiu_agent
# Open http://127.0.0.1:8765
```

Create a mission via the Web UI or API:
```bash
curl -X POST http://localhost:8765/api/missions \
  -H "Content-Type: application/json" \
  -d '{"name":"test","target":"10.0.0.5:8080","goal":"Find and capture all flags","expected_flags":1}'
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

The Kali Docker sandbox includes 200+ pre-installed tools:

- **Network**: nmap, masscan, netcat, socat, chisel, proxychains
- **Web**: sqlmap, gobuster, ffuf, nikto, wpscan, commix
- **Exploit**: searchsploit, metasploit, nuclei, ysoserial
- **Python**: requests, httpx, PyJWT, flask-unsign, impacket, scapy
- **AD/Internal**: smbclient, bloodhound, certipy, crackmapexec
- **Crypto**: john, hashcat, hydra
- **Wordlists**: SecLists, rockyou.txt

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