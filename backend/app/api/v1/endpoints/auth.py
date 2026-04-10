"""
钉钉免登接口

流程：
1. 前端从钉钉 JS-SDK 获取 auth code
2. 前端将 code 传给此接口
3. 后端用 code 向钉钉换取 userid
4. 后端查询/创建用户记录
5. 返回用户身份信息
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/dingtalk", response_model=UserResponse)
async def dingtalk_login(code: str, db: AsyncSession = Depends(get_db)):
    """
    钉钉免登

    - code: 前端从钉钉 JS-SDK dd.runtime.auth 获得的临时授权码
    - 返回: 用户身份信息（uuid、name、role）

    业务逻辑（后续实现）：
      1. 用 code 向钉钉换取 dingtalk_userid
      2. 根据 dingtalk_userid 查找/创建本地 User 记录
    """
    # TODO: 调用钉钉 OAuth2 接口换取 userid
    # TODO: 查询/创建 User 记录
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="钉钉免登功能待实现，请先配置 DINGTALK_* 环境变量",
    )
