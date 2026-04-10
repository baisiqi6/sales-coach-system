# CoachStage 智能销售对练系统

基于钉钉生态的企业级 AI 对练系统

## 项目结构

```
coach-stage/
├── .env.example                # 环境变量模板（docker-compose 使用）
├── docker-compose.yml           # Docker 编排（PostgreSQL + Redis + Backend）
│
├── backend/                     # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/             # API 路由层
│   │   ├── core/                # 核心配置（config, database）
│   │   ├── models/              # 数据库模型（SQLAlchemy 2.0）
│   │   ├── schemas/             # Pydantic 请求/响应模型
│   │   └── services/            # 业务逻辑层（待实现）
│   ├── alembic/                 # 数据库迁移（Alembic 异步模式）
│   ├── requirements.txt
│   ├── Dockerfile
│   └── entrypoint.sh            # 容器启动脚本
│
├── frontend-miniapp/            # uni-app 销售端小程序
│   ├── src/pages/               # 页面（index / chat / report）
│   ├── src/api/                 # API 封装
│   └── src/store/               # Pinia 状态管理
│
└── frontend-admin/              # Vue3 主管后台（待实现）
```

## 快速开始

### 前置条件

- Docker + Docker Compose
- （可选）前端开发：HBuilderX 或 uni-app CLI

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入真实凭据（POSTGRES_PASSWORD、REDIS_PASSWORD、DINGTALK_*、LLM_* 等）
```

### 2. 启动所有服务

```bash
docker compose up --build
```

服务启动顺序：
1. `postgres` → 健康检查通过
2. `redis` → 健康检查通过
3. `backend` → 运行 `alembic upgrade head` 迁移数据库 → 启动 uvicorn

### 3. 验证服务

```bash
# 基础健康检查
curl http://localhost:8000/health

# API 健康检查
curl http://localhost:8000/api/v1/health

# 查看 Swagger 文档
open http://localhost:8000/docs
```

### 4. 查看服务状态和日志

```bash
docker compose ps           # 查看运行状态
docker compose logs -f      # 实时日志
docker compose logs backend # 仅 backend 日志
```

### 5. 停止服务

```bash
docker compose down         # 停止并移除容器
docker compose down -v      # 停止并删除数据卷（慎用，会清空数据库）
```

### 6. 本地开发（直接运行 Python，不进容器）

项目使用独立的虚拟环境 `backend/venv/`，完全隔离于全局 Python 环境。

#### 前提：先启动数据库和 Redis（用 Docker）

```bash
# 只启动 postgres 和 redis，不启动 backend 容器
docker compose up -d postgres redis
```

#### 配置 .env

```bash
cp .env.example .env
# 编辑 .env，填入数据库和 Redis 凭据
# 注意：本地开发时需要将 DB_HOST 和 REDIS_HOST 改为 localhost
```

#### 创建 / 激活虚拟环境

```bash
cd backend

# 首次创建（如果 backend/venv 不存在）
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖（只需执行一次）
pip install -r requirements.txt
```

#### 启动后端

```bash
# 首次运行需要迁移数据库
alembic upgrade head

# 启动开发服务器（热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

> 本地开发连接地址：
> - PostgreSQL：`127.0.0.1:5433`（由 docker-compose 映射）
> - Redis：`127.0.0.1:6379`
> - Backend：`http://localhost:8000`

#### 停止虚拟环境

```bash
deactivate
```

#### 注意事项

- **禁止**使用全局 Python 或全局 pip 安装项目依赖，必须在激活 `venv` 后操作。
- 如果遇到 `ModuleNotFoundError`，先确认虚拟环境已激活（命令行前缀显示 `(venv)`）。
- 后端代码改动后 uvicorn 会自动重载（`--reload`），无需手动重启。

## 前端说明

### 编译目标

- **钉钉小程序**（生产）：使用 `dd.getRecorderManager()` 原生录音
- **H5**（开发调试）：在浏览器中运行，录音功能降级

### 打包钉钉小程序（HBuilderX）

1. 打开 `frontend-miniapp` 项目
2. 运行 → 运行到小程序模拟器 → 钉钉小程序
3. 发行 → 小程序-钉钉

## 当前进度

- [x] Docker 容器化部署（PostgreSQL + Redis + Backend）
- [x] 数据库模型层（SQLAlchemy 2.0 Mapped 语法）
- [x] Alembic 异步迁移配置
- [x] Pydantic Schemas 层（API 接口契约）
- [x] API 路由层（模块化路由注册，骨架完成）
- [x] 健康检查接口
- [x] 数据库迁移（entrypoint.sh 自动执行 `alembic upgrade head`）
- [x] Redis 连接层（`core/redis.py`）
- [ ] 钉钉 Stream SDK 集成
- [ ] LLM 服务集成（`services/llm_service.py`）
- [ ] ASR 语音识别（`services/asr_service.py`）
- [ ] TTS 语音合成（`services/tts_service.py`）
- [ ] 对练核心功能（`endpoints/session.py`）
- [ ] 主管后台功能
- [ ] 前端小程序录音 + SSE 通信
