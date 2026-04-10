"""
对练会话表
"""

import uuid
from sqlalchemy import String, Text, Integer, ForeignKey, Enum as SQLEnum, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class SessionStatus:
    IN_PROGRESS = 0   # 对练进行中
    COMPLETED = 1     # 对练已完成
    INTERRUPTED = 2   # 对练中断


class Session(Base, TimestampMixin):
    """
    对练会话表

    记录一次完整的对练会话，从创建到结束的全生命周期。
    """

    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="全局唯一 ID，用于外部暴露",
    )

    # 参与者
    sale_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="参与对练的销售用户 ID",
    )

    persona_id: Mapped[int] = mapped_column(
        ForeignKey("personas.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="对练使用的 AI 分身 ID",
    )

    # 状态与评分
    status: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=SessionStatus.IN_PROGRESS,
        index=True,
        comment="会话状态：0=进行中，1=已完成，2=中断",
    )

    total_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="综合评分（0-100），会话结束后填写",
    )

    # JSONB 字段：结构化但灵活的数据
    score_detail_json: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="分维度评分详情 JSON，如 {'沟通技巧': 85, '产品知识': 72}",
    )

    report_json: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="综合报告 JSON，含扣分点、改进建议等",
    )
