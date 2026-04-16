"""
对练会话 Schema
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class SessionBase(BaseModel):
    """基础会话字段"""
    sale_user_id: int
    persona_id: int | None = None


class SessionCreate(SessionBase):
    """创建对练会话"""
    pass


class SessionEndRequest(BaseModel):
    """
    结束对练请求
    可选携带结束原因等备注
    """
    reason: str | None = None


class SessionResponse(SessionBase):
    """
    会话响应
    total_score 和 report_json 在会话结束后才有值
    """
    uuid: UUID = Field(validation_alias="uid")
    status: int  # 0=进行中, 1=已完成, 2=中断
    total_score: int | None = None
    score_detail_json: dict | None = None
    report_json: dict | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
