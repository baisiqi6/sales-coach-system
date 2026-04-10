"""
主管后台接口

主管查看对练会话列表，对会话进行审核操作（通过/退回）
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.session import SessionResponse

router = APIRouter(prefix="/admin", tags=["主管后台"])


@router.get("/sessions", response_model=list[SessionResponse])
async def list_all_sessions(
    sale_user_id: int | None = Query(None, description="筛选特定销售用户的会话"),
    status: int | None = Query(None, description="按状态筛选：0=进行中，1=已完成，2=中断"),
    skip: int = Query(0, ge=0, description="跳过前 N 条"),
    limit: int = Query(20, ge=1, le=100, description="返回条数上限"),
    db: AsyncSession = Depends(get_db),
):
    """
    会话列表（主管视图）

    支持按销售用户和状态筛选，分页返回
    """
    # TODO: SELECT * FROM sessions WHERE ... ORDER BY created_at DESC LIMIT limit OFFSET skip
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="会话列表查询待实现",
    )


@router.patch("/sessions/{session_id}", response_model=SessionResponse)
async def review_session(
    session_id: int,
    action: str,  # "approve" | "reject"
    comment: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    审核会话（主管操作）

    - action="approve": 标记为已审核通过
    - action="reject": 标记为退回，可附带原因
    """
    # TODO: UPDATE sessions SET review_status=action, review_comment=comment WHERE id=session_id
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="会话审核操作待实现",
    )
