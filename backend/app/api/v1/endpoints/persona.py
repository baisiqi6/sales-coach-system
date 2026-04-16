"""
AI 分身（角色）管理接口

CRUD：创建 / 查询 / 更新 / 删除 分身角色
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.persona import Persona
from app.schemas.persona import PersonaCreate, PersonaUpdate, PersonaResponse

router = APIRouter(prefix="/personas", tags=["分身管理"])


@router.get("", response_model=list[PersonaResponse])
async def list_personas(db: AsyncSession = Depends(get_db)):
    """
    获取分身列表（所有已创建的分身，供销售选择场景）
    """
    result = await db.execute(select(Persona).order_by(Persona.created_at.desc()))
    return result.scalars().all()


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
    persona = Persona(
        name=payload.name,
        scenario_desc=payload.scenario_desc,
        system_prompt=payload.system_prompt,
    )
    db.add(persona)
    await db.flush()
    await db.refresh(persona)
    return persona


@router.get("/{persona_id}", response_model=PersonaResponse)
async def get_persona(persona_id: int, db: AsyncSession = Depends(get_db)):
    """
    获取单个分身详情
    """
    result = await db.execute(select(Persona).where(Persona.id == persona_id))
    persona = result.scalar_one_or_none()
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分身不存在",
        )
    return persona


@router.put("/{persona_id}", response_model=PersonaResponse)
async def update_persona(
    persona_id: int,
    payload: PersonaUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    更新分身（主管操作）
    """
    result = await db.execute(select(Persona).where(Persona.id == persona_id))
    persona = result.scalar_one_or_none()
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分身不存在",
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(persona, field, value)
    await db.flush()
    await db.refresh(persona)
    return persona


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_persona(persona_id: int, db: AsyncSession = Depends(get_db)):
    """
    删除分身（主管操作）
    """
    result = await db.execute(select(Persona).where(Persona.id == persona_id))
    persona = result.scalar_one_or_none()
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分身不存在",
        )
    await db.delete(persona)
