"""
v1 API 统一路由注册

所有 v1 下的 endpoint router 在此汇总，
最终在 app/main.py 中通过 api_router 注册到 FastAPI 实例。
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    auth,
    persona,
    session,
    evaluation,
    admin,
)

api_router = APIRouter()

# 健康检查
api_router.include_router(health.router)

# 认证
api_router.include_router(auth.router)

# AI 分身管理
api_router.include_router(persona.router)

# 对练会话
api_router.include_router(session.router)

# 评估报告
api_router.include_router(evaluation.router)

# 主管后台
api_router.include_router(admin.router)
