# PikaQiu Agent

PikaQiu Agent 是一个面向 CTF、靶场和授权测试环境的自动化渗透测试 Agent。它通过主 LLM 执行 ReAct 循环，在 Kali Docker 沙箱里运行命令，结合记忆压缩、离线知识库、Skill 和被动 Observer 完成目标分析、利用验证和 Flag 捕获。

## 快速启动

### 1. 安装 Python 依赖

```powershell
cd F:\project\pikaqiu
python -m pip install -r requirements.txt
```

### 2. 配置模型

项目优先读取 `config.yml`，也可以用 `.env` 保存密钥。建议不要把真实 API Key 提交到 Git。

当前默认模型配置使用 OpenAI 兼容 Responses API：

```yaml
llm:
  base_url: "https://www.inroi.shop"
  model: "gpt-5.5"
  reasoning_effort: "xhigh"
  use_responses_api: true
  disable_response_storage: true
```

`.env` 示例：

```powershell
OPENAI_API_KEY=replace-with-your-api-key
PIKAQIU_LLM_API_KEY=replace-with-your-api-key
```

Observer 默认复用主模型配置。它是被动审核器，不是主 Agent 可调用工具；每轮结束后会基于当前运行轨迹和当前记忆介入审核一次。每次审核都会输出 `OK`、`WATCH`、`L1`、`L2`、`L3`、`L4` 或 `ENV` 结论；`OK/WATCH` 只记录和观察，只有明确的 `L*` 或 `ENV` 才会打断/纠偏主 Agent。

### 3. 启动沙箱容器

默认会启动 5 个独立沙箱容器（`pikaqiu-sandbox-1` 到 `pikaqiu-sandbox-5`），最多支持 5 个 Agent 并发执行；每个 Agent 会绑定自己的容器和独立 workspace volume。

```powershell
docker compose up -d
docker compose ps
1..5 | % { docker exec "pikaqiu-sandbox-$_" bash -lc "pwd && python3 --version" }
```

如果本地没有镜像，先构建：

```powershell
docker build -f Dockerfile.sandbox -t pikaqiu-kali-sandbox .
docker compose up -d
```

### 4. 启动 Web UI

```powershell
python -m pikaqiu_agent
```

打开：

```text
http://127.0.0.1:8001
```

配置页：

```text
http://127.0.0.1:8001/settings.html
```

## 前端开发

当前前端已经迁移为 React + Vite + TypeScript。源码在 `frontend/`，构建产物输出到 `pikaqiu_agent/static/`，由 Flask 直接服务。

### 安装前端依赖

```powershell
cd F:\project\pikaqiu\frontend
npm install
```

### 开发模式

先启动后端：

```powershell
cd F:\project\pikaqiu
python -m pikaqiu_agent
```

再启动 Vite：

```powershell
cd F:\project\pikaqiu\frontend
npm run dev
```

访问：

```text
http://127.0.0.1:5173
```

Vite 会把 `/api/*` 代理到 `http://127.0.0.1:8001`。

### 构建前端

```powershell
cd F:\project\pikaqiu\frontend
npm run build
```

构建会执行：

1. 清理旧的 `pikaqiu_agent/static/assets/`
2. TypeScript 类型检查
3. Vite 构建并输出 `index.html`、`settings.html` 和静态资源

构建后只需要运行：

```powershell
cd F:\project\pikaqiu
python -m pikaqiu_agent
```

## 当前前端能力

- Mission Control 首页：创建任务、选择任务、查看运行状态和 Flag。
- 任务详情：总览、时间线、Observer、记忆、证据、知识库检索和 Experience Craft 复验。
- 操作按钮：继续、停止、删除单个任务。
- 人工协作：开启任务指导通道，并向运行中的任务提交 guidance。
- Experiment 归档：保存 challenge code、难度、结果、失败原因、关键参数和备注。
- 设置页：热更新主模型、Observer、Agent 参数、Skill 和知识库相关配置。
- 状态处理：包含加载态、空态、错误提示和移动端布局。

## 系统架构

```text
User
  |
  v
React + Vite Web UI
  |
  v
Flask API (pikaqiu_agent/web_app.py)
  |
  +-- Orchestrator
  |     |
  |     +-- Main Agent LLM
  |     +-- Memory Agent
  |     +-- Passive Observer
  |
  +-- Sandbox Executor
  |     |
  |     +-- Docker containers: pikaqiu-sandbox-1..5
  |
  +-- Knowledge Base
  |     |
  |     +-- RAG / FTS search
  |     +-- CVE / PoC index
  |     +-- Human-reviewed distilled experience
  |
  +-- Skill Loader
  |
  +-- SQLite Storage
```

## 任务工作流

1. 用户在 Web UI 创建 mission，填写目标、目标说明、轮数、命令数、超时和预期 Flag 数。
2. Flask API 调用 Orchestrator 创建任务记录，并启动后台 mission 线程。
3. 主 Agent 读取目标、记忆、知识库结果和已激活 Skill，生成下一步动作。
4. Sandbox Executor 在 `pikaqiu-sandbox-1` 中执行 bash/python 等命令。
5. 命令输出写入 SQLite events，并触发 Flag 自动识别。
6. Memory Agent 默认每 8 次主模型调用后，将新增工具证据压缩成结构化记忆；连续停滞时同一 Memory Agent 会以 `stall_rebase` 模式重整记忆，保留可复现实验证据并把误导路线移入 `dead_ends`。
7. Passive Observer 在每轮结束后审核运行轨迹，并输出 `OK/WATCH/L1/L2/L3/L4/ENV` 结论；`WATCH` 只提醒下一轮观察点，`L*` 或 `ENV` 才注入短纠偏。
8. 前端每 3 秒轮询 mission、detail、experiment 数据并刷新 UI。
9. 达到目标、捕获足够 Flag、达到最大轮数或用户停止后，任务进入终态。
10. 如果任务成功捕获 Flag，系统会自动提炼 `Experience Craft` 草稿，记录漏洞类型、适用场景、Payload、命令链和证据；草稿不会直接进入主 Agent 的经验检索。
11. 人工在前端知识库页复验 craft，批准后才写入 `.pikaqiu_agent/experience_distilled/`，之后才会被主 Agent 作为可复用经验提示检索到；驳回则只保留审查记录。

## 关键目录

```text
pikaqiu_agent/
  __main__.py          Python module entrypoint
  web_app.py           Flask Web backend and REST API
  orchestrator.py      Mission execution and ReAct loop
  llm_client.py        LLM client wrapper
  prompts.py           System prompts and context assembly
  tools.py             Agent tool definitions
  sandbox.py           Docker sandbox command execution
  memory.py            Memory compression and normalization
  observer_runtime.py  Passive Observer runtime
  knowledge.py         Knowledge indexing and search
  skill_loader.py      SKILL.md discovery and activation
  storage.py           SQLite persistence
  static/              Built frontend served by Flask

frontend/
  src/                 React + TypeScript source
  scripts/             Build helper scripts
  package.json         Frontend commands and dependencies
  vite.config.ts       Vite config, builds into pikaqiu_agent/static

knowledge/             Offline knowledge base source files
skills/                Local skills, one SKILL.md per skill
config.yml             Main configuration
docker-compose.yml     Sandbox container orchestration
Dockerfile.sandbox     Kali sandbox image definition
requirements.txt       Python dependencies
```

## 常用 API

创建任务：

```powershell
curl -X POST http://127.0.0.1:8001/api/missions `
  -H "Content-Type: application/json" `
  -d "{\"name\":\"pikaqiu-target\",\"target\":\"http://127.0.0.1:8080\",\"goal\":\"Find and capture all flags\",\"expected_flags\":1}"
```

查看任务列表：

```powershell
curl http://127.0.0.1:8001/api/missions
```

查看任务详情：

```powershell
curl http://127.0.0.1:8001/api/missions/<mission_id>
```

知识库检索：

```powershell
curl "http://127.0.0.1:8001/api/knowledge/search?q=file%20upload&limit=8"
```

查看待复验经验草稿：

```powershell
curl http://127.0.0.1:8001/api/experience/crafts
```

批准经验草稿入库：

```powershell
curl -X POST http://127.0.0.1:8001/api/experience/crafts/<craft_id>/approve `
  -H "Content-Type: application/json" `
  -d "{\"reviewer\":\"human\",\"notes\":\"payload reproduced in clean sandbox\"}"
```

驳回经验草稿：

```powershell
curl -X POST http://127.0.0.1:8001/api/experience/crafts/<craft_id>/reject `
  -H "Content-Type: application/json" `
  -d "{\"reviewer\":\"human\",\"notes\":\"could not reproduce\"}"
```

查看 Skills：

```powershell
curl http://127.0.0.1:8001/api/skills
```

## 知识库

默认知识库目录是 `knowledge/`，由 `knowledge_dir` 控制。当前后端会在启动时确保索引可用。

支持：

- 目录递归索引
- ZIP 包自动解压和索引
- RAG / FTS 检索
- `.pikaqiu_agent/experience_distilled/` 中已经人工批准的成功经验

前端的知识库页调用：

```text
GET /api/knowledge/search
POST /api/knowledge/reindex
GET /api/experience/crafts
GET /api/experience/crafts/<craft_id>
POST /api/experience/crafts/<craft_id>/approve
POST /api/experience/crafts/<craft_id>/reject
```

## Skills

默认目录是 `skills/`。每个 Skill 使用一个 `SKILL.md`：

```text
skills/
  builtin/
    recon/
      SKILL.md
```

基本格式：

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

任务创建时可以手动指定 Skills：

```powershell
curl -X POST http://127.0.0.1:8001/api/missions `
  -H "Content-Type: application/json" `
  -d "{\"name\":\"target\",\"target\":\"http://127.0.0.1:8080\",\"goal\":\"Find flag\",\"skills\":[\"recon\"]}"
```

当 `skills_auto_use` 为 true 时，主 Agent 也可以在任务过程中通过 Skill 搜索和激活机制自动加载相关 Skill。

## 配置速查

| 字段 | 默认含义 |
| --- | --- |
| `llm_base_url` | 主模型 API 地址 |
| `llm_model` | 主模型名称 |
| `llm_reasoning_effort` | 推理强度 |
| `llm_use_responses_api` | 是否使用 Responses API |
| `llm_disable_response_storage` | 是否禁用响应存储 |
| `compression_model` | 轮内上下文语义压缩模型，默认 `gpt-5.5` |
| `compression_reasoning_effort` | 压缩模型推理强度，默认 `low` |
| `compression_timeout_sec` | 压缩模型调用超时，默认 180 秒 |
| `initial_rounds` | 新任务默认最大轮数 |
| `initial_commands` | 新任务默认每轮命令数 |
| `command_timeout_sec` | 单条沙箱命令超时 |
| `stdout_limit` | 命令输出截断长度 |
| `memory_compress_interval` | 结构化记忆压缩间隔，按主模型调用次数计，默认 8 |
| `disable_memory_rebase` | 是否禁用连续停滞时的 Memory Agent 记忆重整 |
| `knowledge_top_k` | 注入上下文的知识库结果数 |
| `skills_dir` | Skill 根目录 |
| `skills_auto_use` | 是否允许主 Agent 自动搜索和激活 Skill |

## 验证命令

```powershell
cd F:\project\pikaqiu\frontend
npm run build

cd F:\project\pikaqiu
python -m pikaqiu_agent
```

另开一个终端：

```powershell
curl http://127.0.0.1:8001/api/bootstrap
curl http://127.0.0.1:8001/
curl http://127.0.0.1:8001/settings.html
```
