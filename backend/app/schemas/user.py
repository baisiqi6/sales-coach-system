"""
用户 Schema
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """基础用户字段，各场景通用"""
    name: str
    role: str  # "SALE" or "MANAGER"


class UserCreate(UserBase):
    """创建用户"""
    dingtalk_userid: str


class UserUpdate(BaseModel):
    """更新用户（全部字段可选）"""
    name: str | None = None
    role: str | None = None


class UserResponse(UserBase):
    """用户响应（API 返回给前端）"""
    uuid: str = Field(validation_alias="uid")
    dingtalk_userid: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
