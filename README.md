# pikaqiu-agent

精简版 SRC 测试 Agent 工程。

## 核心模块

- reasoning agent：识别功能点、映射测试家族、扩展任务树
- act agent：选择待执行节点并调用本地工具
- parsing agent：压缩执行输出并回填状态

## 环境要求

- Python >= 3.11
- Node.js >= 18

## 快速开始

Windows（conda base）：

```powershell
conda activate base
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

Copy-Item .env.example .env

cd frontend
npm install
cd ..
```

Linux（venv）：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

cp .env.example .env

cd frontend
npm install
cd ..
```

## 配置说明

项目默认读取根目录 `.env`。

最小可用配置示例：

```dotenv
ANTHROPIC_MODEL=deepseek-reasoner
ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
ANTHROPIC_AUTH_TOKEN=你的网关令牌
```

说明：

- `ANTHROPIC_BASE_URL` 不能写成原生 `.../chat/completions`
- 三个 agent 会自动创建独立运行目录：
  - `.runtime_workspaces/reasoning`
  - `.runtime_workspaces/act`
  - `.runtime_workspaces/parsing`

## 后端运行（CLI）

```powershell
pikaqiu "Admin login endpoint /api/login exposes username password captcha and token-based session handling."
```

等价命令：

```powershell
python -m cli "Admin login endpoint /api/login exposes username password captcha and token-based session handling."
```

说明：

- Windows 请在 conda base 环境内执行上述命令。
- Linux 请先激活 .venv 后再执行上述命令。

## 后端服务运行（前端联调）

```powershell
pikaqiu-api
```

等价命令：

```powershell
python -m uvicorn api_server:app --app-dir src --host 0.0.0.0 --port 8000
```

说明：

- Windows 请在 conda base 环境内执行。
- Linux 请先激活 .venv 后执行。

接口：

- `GET /api/health`
- `GET /api/runs`
- `GET /api/runs/latest`
- `GET /api/runs/{run_id}`
- `POST /api/runs`

## RAG 知识库服务（使用本地 vulnerabilities）

默认知识源目录为 `src/rag/vulnerabilities`。

1) 先构建向量库（会生成 `src/rag/faiss_db`）：

```powershell
python src/rag/rag_kdprepare.py
```

2) 启动知识库服务（默认端口 `8081`）：

```powershell
python src/rag/knowledge_service.py
```

3) 健康检查：

```powershell
curl http://127.0.0.1:8081/health
```

可选：若需切换知识源目录，可设置环境变量 `RAG_KB_DIR`（支持绝对路径，或相对 `src` 的路径）。

## 前端运行

```powershell
cd frontend
npm run dev
```

默认地址：`http://127.0.0.1:5173`

默认会通过 Vite 代理把 `/api/*` 转发到 `http://127.0.0.1:8000`。

若本机 `8000` 端口不可用，可改用环境变量：

```powershell
$env:PIKAQIU_API_PORT = "8001"
$env:PIKAQIU_API_TARGET = "http://127.0.0.1:8001"
```

然后分别启动后端与前端。

联调顺序：

1. 启动后端 API 服务
2. 启动前端 `npm run dev`
3. 在页面输入功能描述，点击“启动真实运行”

## 测试

后端：

```powershell
python -m pytest
```

前端构建：

```powershell
cd frontend
npm run build
```

## 目录

```text
src/
├─ cli.py
├─ settings.py
├─ workflow.py
├─ agents/
├─ core/
├─ infra/
├─ reasoning/
└─ runtime/
   ├─ base.py
   └─ provider.py
```
