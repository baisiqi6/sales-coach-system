"""
AI 分身 Schema
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PersonaBase(BaseModel):
    """基础分身字段"""
    name: str
    scenario_desc: str
    system_prompt: str


class PersonaCreate(PersonaBase):
    """创建分身（主管操作）"""
    pass


class PersonaUpdate(BaseModel):
    """更新分身（全部字段可选）"""
    name: str | None = None
    scenario_desc: str | None = None
    system_prompt: str | None = None


class PersonaResponse(PersonaBase):
    """分身响应"""
    uuid: str = Field(validation_alias="uid")
    created_by_manager_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
