#!/bin/sh
# =====================================================================
# CoachStage Backend 启动脚本
# 由 Dockerfile ENTRYPOINT 调用
# =====================================================================

set -e

# ---- 等待 PostgreSQL 就绪 ----
echo "[entrypoint] 等待 PostgreSQL 就绪..."
until pg_isready -h postgres -U "${DB_USER}" -d "${DB_NAME}"; do
  echo "[entrypoint] PostgreSQL 未就绪，3 秒后重试..."
  sleep 3
done
echo "[entrypoint] PostgreSQL 已就绪"

# ---- 等待 Redis 就绪 ----
echo "[entrypoint] 等待 Redis 就绪..."
until redis-cli -h redis -a "${REDIS_PASSWORD}" ping > /dev/null 2>&1; do
  echo "[entrypoint] Redis 未就绪，3 秒后重试..."
  sleep 3
done
echo "[entrypoint] Redis 已就绪"

# ---- 数据库迁移 ----
echo "Running database migrations..."
python -m alembic upgrade head
echo "Database migrations complete."

# ---- 启动 FastAPI ----
echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
