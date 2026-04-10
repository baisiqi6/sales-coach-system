"""
AI 分身（角色）表
"""

import uuid
from sqlalchemy import String, Text, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Persona(Base, TimestampMixin):
    """
    AI 分身（角色）表

    由主管创建，定义对练场景的 System Prompt。
    常见的分身类型：客户、竞品销售、刁难型客户等。
    """

    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="全局唯一 ID，用于外部暴露",
    )

    name: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        comment="分身名称，如'价格异议客户'",
    )

    scenario_desc: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
        comment="场景描述，展示给销售看的简短说明",
    )

    system_prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="核心字段：LLM System Prompt，定义 AI 分身的行为",
    )

    # 创建者（主管）
    created_by_manager_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="创建该分身的主管用户 ID",
    )
