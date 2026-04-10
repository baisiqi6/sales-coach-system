"""
用户表
"""

import uuid
from sqlalchemy import String, Enum as SQLEnum, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class UserRole(str):
    SALE = "SALE"
    MANAGER = "MANAGER"


user_roles = ["SALE", "MANAGER"]


class User(Base, TimestampMixin):
    """
    用户表

    钉钉免登后创建/更新，dingtalk_userid 是唯一身份标识。
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        comment="全局唯一 ID，用于外部暴露",
    )

    dingtalk_userid: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
        comment="钉钉用户唯一 ID",
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False, comment="用户姓名")
    role: Mapped[str] = mapped_column(
        SQLEnum("SALE", "MANAGER", name="user_role", native_enum=False),
        nullable=False,
        default="SALE",
        comment="角色：SALE=销售，MANAGER=主管",
    )

    __table_args__ = (
        UniqueConstraint("dingtalk_userid", name="uq_users_dingtalk_userid"),
    )
