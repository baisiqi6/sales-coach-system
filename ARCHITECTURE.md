# CoachStage 智能销售对练系统 - 架构文档

> 本文档定义项目技术选型、目录结构、核心模块职责及约束规则。所有实现必须严格遵循本文档。

---

## 一、技术选型清单

### 1.1 核心架构（确定路线，不可轻易替换）

| 模块 | 技术选型 | 选型原因 |
|------|---------|---------|
| 前端销售端 | uni-app (Vue 3 + TypeScript + Vite) | 解决 H5 在钉钉内录音权限不稳定的问题，编译为钉钉小程序后使用 `dd.getRecorderManager()` 原生录音；开发阶段编译为 H5 在浏览器调试 |
| 后端服务 | Python 3.11+ + FastAPI | AI 生态最完善，原生支持异步，适合处理 LLM 流式输出（SSE）和高并发语音流 |
| 钉钉集成 | dingtalk-stream (Python SDK) | 无需公网 IP、无需 HTTPS 域名证书，通过 WebSocket 长连接接收/发送钉钉机器人消息 |
| LLM 调用 | OpenAI 兼容接口格式（通过 One-API 或官方适配器） | 底层 LLM（DeepSeek / 通义千问）可随时无缝切换，业务代码零改动 |
| 前端录音 | `dd.getRecorderManager()`（仅限小程序环境） | 原生级稳定性，支持后台录音和标准 MP3 格式输出 |

### 1.2 灵活路线（可根据实际情况替换或补充）

| 模块 | 默认推荐 | 可替换方案 |
|------|---------|-----------|
| UI 组件库 | uv-ui | uView Plus / uni-ui |
| 图表库 | uCharts（小程序）/ ECharts（PC 管理端） | - |
| 数据库 | PostgreSQL 16 + 挂载卷持久化 | - |
| 缓存 | Redis（存钉钉 access_token 和流式对话上下文） | - |
| ASR（语音转文字） | Whisper API | 阿里云 ASR |
| TTS（文字转语音） | MVP: edge-tts（Python 免费库，音质极好）；商业化后 | 阿里云 CosyVoice |
| PC 管理后台 | Vue 3 + Element Plus | - |
| 外部知识库对接 | 只要对方提供 HTTP API（如 `POST /api/search`），直接用 `httpx` 调用，不绑定特定厂商 | - |

### 1.3 核心技术栈约束

> 以下约束为强制要求，实现时不得违反。

- **Python**: 3.11+
- **后端框架**: FastAPI（异步）
- **ORM**: SQLAlchemy 2.0（**必须使用 `Mapped` 和 `mapped_column` 新式声明**）
- **数据库驱动**: asyncpg（PostgreSQL 异步驱动）
- **迁移工具**: Alembic（异步迁移）
- **配置管理**: Pydantic v2（`pydantic-settings`）
- **数据库**: PostgreSQL 16（**必须使用 JSONB 字段类型**）

---

## 二、项目目录结构

```
coach-stage/
├── .env.example                # 环境变量模板（docker-compose 使用）
├── docker-compose.yml           # Docker 编排（PostgreSQL + Redis + Backend）
│
├── backend/                     # FastAPI 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 入口，路由挂载
│   │   ├── api/                 # 路由层
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py    # 统一注册所有 v1 路由
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── health.py     # 健康检查
│   │   │           ├── auth.py       # 钉钉免登
│   │   │           ├── persona.py    # 分身管理 CRUD
│   │   │           ├── session.py    # 对练核心流（SSE + 录音接收）
│   │   │           ├── evaluation.py # 打分报告查询
│   │   │           └── admin.py      # 主管后台 API
│   │   ├── core/                # 核心配置与初始化
│   │   │   ├── __init__.py
│   │   │   ├── config.py        # pydantic-settings 环境变量
│   │   │   ├── database.py      # SQLAlchemy async engine + session
│   │   │   ├── redis.py         # Redis 连接初始化（待实现）
│   │   │   └── dingtalk.py      # 钉钉 Stream 客户端初始化（待实现）
│   │   ├── models/              # 数据库模型（SQLAlchemy 2.0 Mapped）
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Base + TimestampMixin（所有表通用）
│   │   │   ├── user.py          # 用户表
│   │   │   ├── persona.py       # AI 分身（角色）表
│   │   │   ├── session.py       # 对练会话表（含 JSONB 评分字段）
│   │   │   └── message.py       # 消息记录表
│   │   ├── schemas/             # Pydantic 请求/响应模型（API 接口契约）
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── persona.py
│   │   │   ├── session.py
│   │   │   ├── message.py
│   │   │   └── evaluation.py
│   │   └── services/             # 业务逻辑层（待实现）
│   │       ├── __init__.py
│   │       ├── llm_service.py        # 统一 LLM 调用封装（OpenAI 格式）
│   │       ├── asr_service.py       # 语音转文本
│   │       ├── tts_service.py       # 文本转语音
│   │       ├── rag_service.py       # 外部知识库 API 对接
│   │       └── prompt_templates.py   # 所有 Prompt 模板集中管理
│   ├── alembic/                 # 数据库迁移（Alembic 异步模式）
│   │   ├── env.py               # 异步迁移环境配置
│   │   ├── script.py.mako       # 迁移文件模板
│   │   └── versions/             # 迁移脚本存放目录
│   ├── alembic.ini              # Alembic 配置（sqlalchemy.url 动态注入）
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── entrypoint.sh             # 容器启动脚本（等待 DB + 迁移 + 启动 uvicorn）
│   ├── .env                      # 本地开发环境变量（已加入 .gitignore）
│   └── .env.example              # 环境变量模板（容器内使用）
│
├── frontend-miniapp/             # uni-app 销售端
│   ├── App.vue                   # 应用入口
│   ├── main.js                   # JS 入口
│   ├── manifest.json              # uni-app 配置（编译目标选钉钉小程序）
│   ├── pages.json                 # 页面路由配置
│   ├── src/
│   │   ├── api/
│   │   │   └── index.js          # 封装后端所有 API 请求
│   │   ├── store/
│   │   │   └── index.js          # Pinia 状态管理
│   │   └── pages/
│   │       ├── index/            # 首页（场景列表 + 开始对练）
│   │       ├── chat/             # 对练房间（核心：录音控制、SSE 接收、音频播放）
│   │       └── report/           # 报告页（雷达图渲染 + 扣分点列表）
│   └── static/                   # 静态资源（tab 图标等）
│
└── frontend-admin/               # Vue3 主管后台（待实现，可独立仓库）
    └── src/views/
        ├── dashboard/            # 数据看板
        └── session-review/       # 任务审核列表（退回/通过操作）
```

---

## 三、核心模块职责

### 3.1 后端模块

| 模块 | 职责 | 状态 |
|------|------|------|
| `api/v1/endpoints/auth.py` | 钉钉免登：接收钉钉授权 code，换取用户身份 | 骨架 |
| `api/v1/endpoints/persona.py` | AI 分身（角色）CRUD | 骨架 |
| `api/v1/endpoints/session.py` | **对练核心流**：接收前端录音，SSE 推送 LLM 回复音频流 | 骨架 |
| `api/v1/endpoints/evaluation.py` | 打分报告查询 | 骨架 |
| `api/v1/endpoints/admin.py` | 主管后台 API | 骨架 |
| `core/config.py` | 所有环境变量统一管理（数据库/Redis/钉钉/LLM/ASR/TTS） | ✅ 完成 |
| `core/database.py` | SQLAlchemy async engine 和 async session 依赖注入 | ✅ 完成 |
| `core/redis.py` | Redis 连接池管理，提供 `get_redis()` 依赖 | 待实现 |
| `core/dingtalk.py` | 钉钉 Stream SDK 客户端单例初始化 | 待实现 |
| `services/` 全部 | LLM / ASR / TTS / RAG 业务逻辑封装 | 待实现 |

### 3.2 前端核心页面

| 页面 | 职责 |
|------|------|
| `pages/index/index.vue` | 首页：展示对练场景列表，点击后进入 `chat` 页面 |
| `pages/chat/chat.vue` | 对练房间：录音控制（`dd.getRecorderManager()`）、SSE 接收 LLM 流式响应、`AudioContext` 播放 TTS 音频流 |
| `pages/report/report.vue` | 报告页：渲染雷达图（评分维度）、展示扣分点列表和建议 |

---

## 四、API 设计概要

### 4.1 路由前缀规范

所有 API 统一前缀：`/api/v1/`

### 4.2 核心端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/health` | 健康检查 |
| GET | `/api/v1/ping` | Ping 测试 |
| POST | `/api/v1/auth/dingtalk` | 钉钉免登（code 换 token） |
| GET | `/api/v1/personas` | 获取分身列表 |
| POST | `/api/v1/personas` | 创建分身 |
| GET | `/api/v1/personas/{id}` | 获取分身详情 |
| PUT | `/api/v1/personas/{id}` | 更新分身 |
| DELETE | `/api/v1/personas/{id}` | 删除分身 |
| POST | `/api/v1/sessions` | 创建对练会话 |
| GET | `/api/v1/sessions/{id}` | 获取会话详情 |
| POST | `/api/v1/sessions/{id}/message` | 上传用户语音，获取 LLM 回复（SSE 流） |
| POST | `/api/v1/sessions/{id}/end` | 结束对练，生成综合报告 |
| GET | `/api/v1/evaluations/{session_id}` | 获取会话评估报告 |
| GET | `/api/v1/admin/sessions` | 主管：会话列表（支持筛选/分页） |
| PATCH | `/api/v1/admin/sessions/{id}` | 主管：审核操作（通过/退回） |

---

## 五、数据流概要

### 5.1 对练核心流程

```
用户（小程序）
    ↓ POST /sessions/{id}/message + 录音文件（MP3）
ASR（Whisper）: MP3 → 文本
    ↓
LLM（DeepSeek/通义千问）: 上下文 + 用户输入 → 流式文本响应
    ↓
RAG（可选）: 补充知识库上下文
    ↓
TTS（edge-tts / MiniMax M2.7）: 文本 → 音频流
    ↓
[SSE 推送] → 前端 AudioContext 播放
    ↓
评估服务: 记录本轮打分 → 写入 score_detail_json
```

### 5.2 钉钉机器人消息流

```
钉钉服务器 → [WebSocket 长连接] → dingtalk-stream SDK → 回调处理 → 回复消息
```

---

## 六、开发约束

1. **Python 后端必须使用 `async`/`await`**：所有数据库操作、Redis 操作、LLM 调用、TTS/ASR 调用均为异步。
2. **数据库模型必须使用 SQLAlchemy 2.0 新式声明**：`Mapped[int]`、`mapped_column(String)`，禁止使用旧式 `Column()`。
3. **JSONB 字段**：结构化但需灵活扩展的字段（如评估报告、对话上下文摘要）必须使用 `JSONB` 而非普通 `JSON`。
4. **LLM 调用不绑定厂商**：所有 LLM 调用经由 `services/llm_service.py` 统一封装，业务代码不直接 import 任何特定 LLM SDK。
5. **RAG 服务不绑定厂商**：所有外部知识库调用经由 `services/rag_service.py` 统一封装。
6. **前端录音必须条件判断**：使用 `dd.getRecorderManager()` 时必须判断是否处于小程序环境，开发阶段为 H5 时降级处理。
7. **敏感信息不上传**：`.env` 文件不提交，`.env.example` 作为模板。
8. **SSE 响应禁止缓存**：`Cache-Control: no-cache`，防止前端 SSE 连接不更新。

---

## 七、环境变量清单

### 7.1 项目根目录 `.env.example`（docker-compose 使用）

```
# PostgreSQL 凭据（postgres 服务初始化 + backend 环境注入）
POSTGRES_DB=coach_stage
POSTGRES_USER=coach_user
POSTGRES_PASSWORD=change_me_in_production

# Redis 凭据
REDIS_PASSWORD=change_me_in_production

# 钉钉开放平台
DINGTALK_APP_KEY=your_dingtalk_app_key
DINGTALK_APP_SECRET=your_dingtalk_app_secret
DINGTALK_CLIENT_ID=your_dingtalk_client_id
DINGTALK_CLIENT_SECRET=your_dingtalk_client_secret
DINGTALK_STREAM_TOPIC=/v1.0/im/bot/messages/get_by_app

# LLM（OpenAI 兼容格式）
LLM_API_BASE=https://api.deepseek.com/v1
LLM_API_KEY=your_llm_api_key
LLM_MODEL=deepseek-chat

# ASR（阿里云语音识别）
ASR_APP_KEY=your_asr_app_key
ASR_ACCESS_KEY_ID=your_access_key_id
ASR_ACCESS_KEY_SECRET=your_access_key_secret
ASR_REGION=cn-wulanchabu

# TTS（MiniMax M2.7-highspeed）
TTS_API_KEY=your_tts_api_key
TTS_MODEL=MiniMax-M2.7-highspeed
TTS_VOICE_ID=your_voice_id

# 外部知识库 RAG
RAG_API_URL=https://your-rag-service/api/search
RAG_API_KEY=your_rag_api_key
```

### 7.2 backend/.env.example（容器内 Python 代码使用）

Python 代码通过 `app/core/config.py` 读取以下变量（由 docker-compose 注入）：

| 变量 | 说明 |
|------|------|
| `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` / `DB_NAME` | 数据库连接字段，`DATABASE_URL` 由 `config.py` 拼接 |
| `REDIS_PASSWORD` / `REDIS_HOST` / `REDIS_PORT` / `REDIS_DB` | Redis 连接字段，`REDIS_URL` 由 `config.py` 拼接 |
| `LLM_API_BASE` / `LLM_API_KEY` / `LLM_MODEL` | LLM 配置 |
| `ASR_*` | 阿里云 ASR 配置 |
| `TTS_*` | MiniMax TTS 配置 |
| `RAG_*` | 知识库配置 |

---

## 八、Docker 部署说明

### 8.1 启动所有服务

```bash
# 1. 复制环境变量模板
cp .env.example .env
# 编辑 .env，填入真实凭据

# 2. 启动全部服务（postgres + redis + backend）
docker compose up --build

# 3. 查看服务状态
docker compose ps

# 4. 查看 backend 日志
docker compose logs -f backend
```

### 8.2 健康检查

```bash
# 基础健康检查（Docker healthcheck）
curl http://localhost:8000/health

# 完整健康检查（走 /api/v1）
curl http://localhost:8000/api/v1/health
```

### 8.3 数据库迁移

首次启动或模型变更后，`entrypoint.sh` 会自动执行 `alembic upgrade head`。手动执行：

```bash
docker compose exec backend alembic revision --autogenerate -m "migration name"
docker compose exec backend alembic upgrade head
```

### 8.4 端口说明

| 服务 | 宿主机端口 | 容器内端口 | 访问地址 |
|------|-----------|-----------|---------|
| backend | 8000 | 8000 | http://localhost:8000 |
| postgres | 未暴露 | 5432 | 仅容器内通过 `postgres:5432` 访问 |
| redis | 未暴露 | 6379 | 仅容器内通过 `redis:6379` 访问 |
