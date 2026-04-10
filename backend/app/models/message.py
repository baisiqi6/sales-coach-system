"""
对话流水表
"""

import uuid
from sqlalchemy import String, Text, ForeignKey, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class MessageRole:
    SALE = "SALE"       # 销售（用户）发送
    AI = "AI"           # AI 分身回复


class Message(Base, TimestampMixin):
    """
    对话流水表

    记录对练过程中的每一条消息，含文本和可选的音频 URL。
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="全局唯一 ID，用于外部暴露",
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="所属对练会话 ID",
    )

    # SALE = 销售发送 / AI = AI 分身回复
    role: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="消息发送方：SALE=销售，AI=AI分身",
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
        comment="消息文本内容",
    )

    audio_url: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        comment="TTS 生成的音频 URL（AI 回复时有值）",
    )

    # 可扩展：存储 ASR 原始结果、LLM token 消耗等
    meta_json: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="元数据 JSON，如 ASR 置信度、LLM 响应时间等",
    )
