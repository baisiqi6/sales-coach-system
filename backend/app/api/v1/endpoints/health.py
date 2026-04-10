"""
健康检查接口
"""

from datetime import datetime
from fastapi import APIRouter, status

from app.core.config import settings

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    健康检查接口
    用于验证服务是否正常运行，以及前后端联通测试
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION,
        "message": f"{settings.APP_NAME} 运行正常",
    }


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    """简单的 ping 接口"""
    return {"pong": True}
