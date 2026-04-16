# CoachStage 智能销售对练系统 - 架构文档

> 本文档定义项目技术选型、目录结构、核心模块职责及约束规则。所有实现必须严格遵循本文档。

---

## 一、技术选型清单

### 1.1 核心架构（确定路线，不可轻易替换）

| 模块 | 技术选型 | 选型原因 |
|------|---------|---------|
| 前端销售端 | uni-app (Vue 3 + Vite) | 编译为钉钉小程序使用原生录音；开发阶段编译为 H5 在浏览器调试 |
| 后端服务 | Python 3.11+ + FastAPI | AI 生态最完善，原生支持异步，适合处理实时语音流 |
| 实时语音框架 | Pipecat | 编排 STT→LLM→TTS Pipeline，内置 VAD、打断处理、轮次管理 |
| 钉钉集成 | dingtalk-stream (Python SDK) | 无需公网 IP，通过 WebSocket 长连接接收/发送钉钉机器人消息 |
| LLM 调用 | DeepSeek（通过 Pipecat DeepSeekLLMService） | 中文效果好，OpenAI 兼容格式，可随时切换底层模型 |

### 1.2 灵活路线（可根据实际情况替换或补充）

| 模块 | 默认推荐 | 可替换方案 |
|------|---------|-----------|
| ASR（语音转文字） | 本地 faster-whisper（GPU 加速） | Deepgram（云端）、阿里云 ASR |
| TTS（文字转语音） | MiniMax Speech（中文效果好） | edge-tts（免费）、Cartesia、ElevenLabs |
| 传输方式 | FastAPI WebSocket + Protobuf 序列化 | Daily.co WebRTC（更低延迟） |
| 数据库 | PostgreSQL 16 + JSONB | - |
| 缓存 | Redis | - |
| PC 管理后台 | Vue 3 + Element Plus | - |
| 外部知识库对接 | 通用 HTTP API | - |

### 1.3 核心技术栈约束

- **Python**: 3.11+
- **后端框架**: FastAPI（异步）
- **ORM**: SQLAlchemy 2.0（**必须使用 `Mapped` 和 `mapped_column` 新式声明**）
- **数据库驱动**: asyncpg（PostgreSQL 异步驱动）
- **迁移工具**: Alembic（异步迁移）
- **配置管理**: Pydantic v2（`pydantic-settings`）
- **数据库**: PostgreSQL 16（**必须使用 JSONB 字段类型**）
- **语音 Pipeline**: Pipecat（所有 STT/LLM/TTS 调用经由 Pipecat 服务抽象）

---

## 二、项目目录结构

```
coach-stage/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 入口，lifespan 管理 + 路由挂载
│   │   ├── api/v1/
│   │   │   ├── router.py        # 统一注册所有 v1 路由
│   │   │   └── endpoints/
│   │   │       ├── health.py         # 健康检查
│   │   │       ├── auth.py           # 钉钉免登
│   │   │       ├── persona.py        # 分身管理 CRUD
│   │   │       ├── session.py        # 对练会话 CRUD（REST）
│   │   │       ├── ws_session.py     # 对练会话 WebSocket（实时语音）
│   │   │       ├── evaluation.py     # 打分报告查询
│   │   │       └── admin.py          # 主管后台 API
│   │   ├── core/
│   │   │   ├── config.py        # 环境变量（含 Whisper/MiniMax/DeepSeek 配置）
│   │   │   ├── database.py      # SQLAlchemy async engine + session
│   │   │   ├── redis.py         # Redis 连接（待实现）
│   │   │   └── dingtalk.py      # 钉钉 Stream（待实现）
│   │   ├── models/              # 数据库模型（SQLAlchemy 2.0）
│   │   ├── schemas/             # Pydantic 请求/响应模型
│   │   ├── services/
│   │   │   └── pipecat_pipeline.py  # Pipecat Pipeline 构建（STT→LLM→TTS）
│   │   └── db/
│   │       └── seed.py          # 种子数据（测试用户 + AI 分身）
│   ├── alembic/                 # 数据库迁移
│   └── requirements.txt
│
├── frontend-miniapp/
│   ├── src/
│   │   ├── api/index.js         # 后端 API 封装
│   │   ├── utils/
│   │   │   ├── protobuf-client.js  # Pipecat protobuf 帧编解码
│   │   │   ├── audio.js            # 音频录制/播放（Web Audio API）
│   │   │   └── websocket.js        # Pipecat WebSocket 客户端
│   │   ├── pages/
│   │   │   ├── index/          # 首页（场景选择）
│   │   │   ├── chat/           # 对练房间（核心页面）
│   │   │   └── report/         # 报告页
│   │   └── store/
│   └── ...
│
└── frontend-admin/              # 主管后台（待实现）
```

---

## 三、核心模块职责

### 3.1 后端模块

| 模块 | 职责 | 状态 |
|------|------|------|
| `endpoints/session.py` | 对练会话 CRUD：创建/查询/结束 | ✅ 完成 |
| `endpoints/ws_session.py` | 对练会话 WebSocket：实时语音通信 | ✅ 完成 |
| `endpoints/persona.py` | AI 分身 CRUD | ✅ 完成 |
| `services/pipecat_pipeline.py` | 构建 Pipecat Pipeline（Whisper→DeepSeek→MiniMax） | ✅ 完成 |
| `core/config.py` | 环境变量管理（含 Whisper/MiniMax/DeepSeek） | ✅ 完成 |
| `core/database.py` | SQLAlchemy async engine + session | ✅ 完成 |
| `main.py` | FastAPI 入口 + lifespan（aiohttp session 管理） | ✅ 完成 |
| `endpoints/auth.py` | 钉钉免登 | 待实现 |
| `endpoints/evaluation.py` | 打分报告查询 | 待实现 |
| `endpoints/admin.py` | 主管后台 API | 待实现 |

### 3.2 前端核心模块

| 模块 | 职责 | 状态 |
|------|------|------|
| `pages/chat/chat.vue` | 对练房间：WebSocket 连接 + 录音 + 消息显示 + 音频播放 | ✅ 完成 |
| `utils/protobuf-client.js` | Pipecat protobuf 帧编解码 | ✅ 完成 |
| `utils/audio.js` | Web Audio API 录音/播放 | ✅ 完成 |
| `utils/websocket.js` | Pipecat WebSocket 客户端 | ✅ 完成 |
| `pages/index/index.vue` | 首页：从后端获取 persona 列表 | ✅ 完成 |

---

## 四、API 设计

### 4.1 REST 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/health` | 健康检查 |
| GET | `/api/v1/personas` | 获取分身列表 |
| POST | `/api/v1/personas` | 创建分身 |
| GET | `/api/v1/personas/{id}` | 获取分身详情 |
| PUT | `/api/v1/personas/{id}` | 更新分身 |
| DELETE | `/api/v1/personas/{id}` | 删除分身 |
| POST | `/api/v1/sessions` | 创建对练会话 |
| GET | `/api/v1/sessions/{id}` | 获取会话详情 |
| POST | `/api/v1/sessions/{id}/end` | 结束对练 |

### 4.2 WebSocket 端点

| 路径 | 描述 |
|------|------|
| `ws://host/api/v1/sessions/{session_uuid}/ws` | 实时语音通信（protobuf 帧格式） |

WebSocket 通信协议：
- **发送**：`InputAudioRawFrame`（PCM 16kHz 16bit 单声道音频）
- **接收**：`TranscriptionFrame`（ASR 转录文本）、`TextFrame`（LLM 流式文本）、`AudioRawFrame`（TTS 音频）

---

## 五、数据流

### 5.1 实时语音对话流程

```
前端（浏览器/小程序）
    ↓ 按住说话 → getUserMedia → PCM 音频帧
    ↓ WebSocket send（protobuf 编码的 AudioRawFrame）
Pipecat Pipeline:
    FastAPIWebsocketTransport.input()
    → WhisperSTTService（本地 faster-whisper, GPU）
    → SileroVADAnalyzer（语音活动检测, stop_secs=0.8）
    → LLMUserAggregator（用户轮次管理）
    → DeepSeekLLMService（system_instruction = persona.system_prompt）
    → MiniMaxHttpTTSService（中文语音合成）
    → FastAPIWebsocketTransport.output()
    → LLMContextAggregatorPair（上下文管理）
    ↓ WebSocket push（protobuf 编码的 TextFrame + AudioRawFrame）
前端
    → TranscriptionFrame → 显示用户消息
    → TextFrame → 流式显示 AI 消息
    → AudioRawFrame → AudioContext 播放
```

### 5.2 会话生命周期

```
1. 前端 POST /sessions → 获取 session_uuid
2. 前端 WebSocket connect /sessions/{uuid}/ws → Pipeline 启动
3. 实时语音对话（多轮）
4. 前端 WebSocket close → Pipeline 结束
5. 前端 POST /sessions/{id}/end → 会话状态更新为 COMPLETED
```

---

## 六、环境变量清单

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `LLM_API_BASE` | DeepSeek API 地址 | `https://api.deepseek.com/v1` |
| `LLM_API_KEY` | DeepSeek API Key | - |
| `LLM_MODEL` | DeepSeek 模型名 | `deepseek-chat` |
| `WHISPER_MODEL` | faster-whisper 模型 | `large-v3-turbo` |
| `WHISPER_DEVICE` | 推理设备 | `cuda` |
| `WHISPER_COMPUTE_TYPE` | 量化类型 | `int8_float16` |
| `TTS_API_KEY` | MiniMax API Key | - |
| `TTS_MODEL` | MiniMax TTS 模型 | `speech-02-turbo` |
| `MINIMAX_GROUP_ID` | MiniMax 群组 ID | - |
| `MINIMAX_VOICE` | MiniMax 音色 | `Calm_Woman` |

---

## 七、开发约束

1. **Python 后端必须使用 `async`/`await`**：所有数据库操作、LLM 调用、TTS/ASR 均为异步。
2. **数据库模型必须使用 SQLAlchemy 2.0 新式声明**：`Mapped[int]`、`mapped_column(String)`。
3. **JSONB 字段**：结构化但需灵活扩展的字段必须使用 `JSONB`。
4. **语音 Pipeline 经由 Pipecat**：所有 STT/LLM/TTS 调用通过 Pipecat 服务抽象，业务代码不直接调用特定 SDK。
5. **前端录音条件判断**：H5 用 Web Audio API，小程序用 `dd.getRecorderManager()`。
6. **敏感信息不上传**：`.env` 文件不提交，`.env.example` 作为模板。
