"""
智能销售对练系统 - FastAPI 后端入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import health
from app.core.config import settings

# 创建 FastAPI 应用
app = FastAPI(
    title="智能销售对练系统 API",
    description="基于钉钉生态的企业级销售对练 AI 系统",
    version="1.0.0",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境需要限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router, prefix="/api/v1", tags=["健康检查"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "智能销售对练系统 API",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
