"""
CoachStage FastAPI 后端入口
"""

from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # Startup
    app.state.aiohttp_session = aiohttp.ClientSession()
    yield
    # Shutdown
    await app.state.aiohttp_session.close()


def create_app() -> FastAPI:
    """应用工厂，方便后续测试时创建独立实例"""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    # ---- CORS 中间件 ----
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---- 路由注册 ----
    # 所有 /api/v1/* 路由统一在 api_router 中管理
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()


# ---- 根路径 ----
@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


# ---- 基础健康检查（用于 Docker healthcheck，不走 /api/v1）----
@app.get("/health")
async def health_check():
    """
    基础健康检查，用于 Docker healthcheck / 前端连通性测试
    """
    return {"status": "ok"}


# ---- 开发调试入口 ----
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
