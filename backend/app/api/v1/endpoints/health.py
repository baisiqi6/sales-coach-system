"""
健康检查接口
"""

from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    timestamp: str
    version: str
    message: str


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    健康检查接口

    用于验证服务是否正常运行，以及前后端联通测试
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        message="智能销售对练系统运行正常"
    )


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    """
    简单的 ping 接口
    """
    return {"pong": True}
