"""
对话消息 Schema
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class MessageBase(BaseModel):
    """基础消息字段"""
    session_id: int
    role: str  # "SALE" or "AI"
    content: str
    audio_url: str | None = None


class MessageCreate(MessageBase):
    """创建消息"""
    meta_json: dict | None = None


class MessageResponse(MessageBase):
    """消息响应"""
    uuid: str = Field(validation_alias="uid")
    meta_json: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
