"""
评估报告接口

获取指定会话的综合评估报告
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.evaluation import EvaluationReport

router = APIRouter(prefix="/evaluations", tags=["评估报告"])


@router.get("/{session_id}", response_model=EvaluationReport)
async def get_evaluation(
    session_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    获取指定会话的综合评估报告

    从 sessions 表读取 score_detail_json 和 report_json 字段
    如果会话未结束（status != COMPLETED），返回 400
    """
    # TODO: SELECT * FROM sessions WHERE id = session_id
    # 检查 status == COMPLETED
    # 读取 score_detail_json / report_json 返回
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="获取评估报告待实现",
    )
