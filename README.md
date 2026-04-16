# CoachStage 智能销售对练系统

基于钉钉生态的企业级 AI 对练系统，使用 Pipecat 实时语音框架实现 STT → LLM → TTS 全链路语音对话。

## 项目结构

```
coach-stage/
├── .env.example                # 环境变量模板（docker-compose 使用）
├── docker-compose.yml           # Docker 编排（PostgreSQL + Redis + Backend）
│
├── backend/                     # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/             # API 路由层
│   │   │   └── endpoints/
│   │   │       ├── session.py      # 对练会话 CRUD（REST）
│   │   │       ├── ws_session.py   # 对练会话 WebSocket（实时语音）
│   │   │       ├── persona.py      # AI 分身 CRUD
│   │   │       └── ...
│   │   ├── core/                # 核心配置（config, database）
│   │   ├── models/              # 数据库模型（SQLAlchemy 2.0）
│   │   ├── schemas/             # Pydantic 请求/响应模型
│   │   ├── services/            # 业务逻辑层
│   │   │   └── pipecat_pipeline.py  # Pipecat 语音 Pipeline（STT→LLM→TTS）
│   │   └── db/
│   │       └── seed.py          # 数据库种子数据
│   ├── alembic/                 # 数据库迁移（Alembic 异步模式）
│   ├── requirements.txt
│   ├── Dockerfile
│   └── entrypoint.sh
│
├── frontend-miniapp/            # uni-app 销售端小程序
│   ├── src/
│   │   ├── pages/               # 页面（index / chat / report）
│   │   ├── api/                 # API 封装
│   │   ├── utils/
│   │   │   ├── protobuf-client.js  # Pipecat protobuf 帧编解码
│   │   │   ├── audio.js            # 音频录制与播放（Web Audio API）
│   │   │   └── websocket.js        # Pipecat WebSocket 客户端
│   │   └── store/               # 状态管理
│   └── ...
│
└── frontend-admin/              # Vue3 主管后台（待实现）
```

## 快速开始

### 前置条件

- Docker + Docker Compose
- Python 3.11+
- （前端）HBuilderX 或 uni-app CLI

### 1. 启动数据库和 Redis

```bash
docker compose up -d postgres redis
```

### 2. 配置环境变量

```bash
cd backend
cp .env.example .env
# 编辑 .env，填入：
# - LLM_API_KEY（DeepSeek）
# - TTS_API_KEY + MINIMAX_GROUP_ID（MiniMax）
# - WHISPER_DEVICE（cuda 或 cpu，取决于服务器是否有 GPU）
```

### 3. 安装依赖并启动后端

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 数据库迁移
alembic upgrade head

# 种子数据（创建测试用户和 AI 分身）
python3 -m app.db.seed

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

### 4. 验证服务

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/personas
```

### 5. 启动前端（H5 模式）

```bash
cd frontend-miniapp
pnpm dev:h5
```

浏览器打开 → 选择场景 → 按住说话 → 听到 AI 回复

## 核心架构

### 语音对话 Pipeline

使用 [Pipecat](https://github.com/pipecat-ai/pipecat) 框架编排实时语音对话：

```
前端（浏览器/小程序）
    ↕ WebSocket（protobuf 帧）
Pipecat Pipeline:
  [FastAPIWebsocketTransport]
  → [WhisperSTTService]    本地 faster-whisper（GPU 加速）
  → [SileroVADAnalyzer]    语音活动检测
  → [DeepSeekLLMService]   DeepSeek 大模型
  → [MiniMaxHttpTTSService] MiniMax 语音合成
  → [FastAPIWebsocketTransport]
    ↕
前端播放音频 + 显示文字
```

### 关键设计

- **WebSocket 双向通信**：替代原 SSE 方案，支持实时音频帧双向传输
- **Protobuf 序列化**：Pipecat 使用 ProtobufFrameSerializer 编解码帧，前端需配套解析
- **VAD + 打断处理**：Pipecat 内置 Silero VAD 检测用户说话，支持用户打断 AI
- **本地 ASR**：faster-whisper 运行在服务器 GPU 上，无需云端 ASR 服务

## 当前进度

- [x] Docker 容器化部署（PostgreSQL + Redis + Backend）
- [x] 数据库模型层（SQLAlchemy 2.0 Mapped 语法）
- [x] Alembic 异步迁移 + 种子数据
- [x] Pydantic Schemas 层（API 接口契约）
- [x] Session / Persona CRUD 端点
- [x] Pipecat 语音 Pipeline（Whisper → DeepSeek → MiniMax）
- [x] WebSocket 实时语音端点
- [x] 前端 WebSocket + 音频录制/播放
- [x] 前端聊天页面（消息显示 + 按住说话）
- [ ] 钉钉 Stream SDK 集成
- [ ] 钉钉小程序端适配（录音 + WebSocket）
- [ ] 逐轮评分 + 评估报告生成
- [ ] RAG 知识库集成
- [ ] 主管后台功能
