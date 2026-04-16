"""
对练会话核心接口

包含：创建会话、获取会话详情、结束会话
实时语音通信通过 WebSocket 端点实现（见 ws_session.py）
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.session import Session, SessionStatus
from app.schemas.session import SessionCreate, SessionResponse, SessionEndRequest

router = APIRouter(prefix="/sessions", tags=["对练会话"])


@router.post("", response_model=SessionResponse, status_code=201)
async def create_session(
    payload: SessionCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    创建对练会话

    前端选择分身后调用此接口创建会话，
    返回会话 uuid 用于后续的 WebSocket 连接
    """
    db_session = Session(
        sale_user_id=payload.sale_user_id,
        persona_id=payload.persona_id,
        status=SessionStatus.IN_PROGRESS,
    )
    db.add(db_session)
    await db.flush()
    await db.refresh(db_session)
    return db_session


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """
    获取会话详情
    """
    result = await db.execute(select(Session).where(Session.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在",
        )
    return session


@router.post("/{session_id}/end", response_model=SessionResponse)
async def end_session(
    session_id: int,
    payload: SessionEndRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    结束对练

    将 session.status 改为 COMPLETED，
    后续可在此生成评估报告
    """
    result = await db.execute(select(Session).where(Session.id == session_id))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在",
        )
    session.status = SessionStatus.COMPLETED
    await db.flush()
    await db.refresh(session)
    return session
