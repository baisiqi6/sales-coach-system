"""
AI 分身（角色）管理接口

CRUD：创建 / 查询 / 更新 / 删除 分身角色
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.persona import PersonaCreate, PersonaUpdate, PersonaResponse

router = APIRouter(prefix="/personas", tags=["分身管理"])


@router.get("", response_model=list[PersonaResponse])
async def list_personas(db: AsyncSession = Depends(get_db)):
    """
    获取分身列表（所有已创建的分身，供销售选择场景）
    """
    # TODO: SELECT * FROM personas ORDER BY created_at DESC
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="分身列表查询待实现",
    )


@router.post("", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
async def create_persona(
    payload: PersonaCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    创建新分身（主管操作）

    - 需要验证当前用户 role == MANAGER（后续实现）
    - system_prompt 是核心字段，决定 AI 分身的行为风格
    """
    # TODO: INSERT INTO personas ...
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="创建分身功能待实现",
    )


@router.get("/{persona_id}", response_model=PersonaResponse)
async def get_persona(persona_id: int, db: AsyncSession = Depends(get_db)):
    """
    获取单个分身详情
    """
    # TODO: SELECT * FROM personas WHERE id = persona_id
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="获取分身详情待实现",
    )


@router.put("/{persona_id}", response_model=PersonaResponse)
async def update_persona(
    persona_id: int,
    payload: PersonaUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    更新分身（主管操作）
    """
    # TODO: UPDATE personas SET ... WHERE id = persona_id
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="更新分身功能待实现",
    )


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_persona(persona_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除分身（主管操作）
    """
    # TODO: DELETE FROM personas WHERE id = persona_id
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="删除分身功能待实现",
    )
