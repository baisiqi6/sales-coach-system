"""
对练会话 WebSocket 端点

实时语音通信：前端通过 WebSocket 连接 Pipecat Pipeline，
发送音频帧，接收转录文本和 TTS 音频。
"""

import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.session import Session
from app.models.persona import Persona
from app.services.pipecat_pipeline import build_and_run_pipeline

router = APIRouter(tags=["对练会话 WebSocket"])


async def _get_system_prompt(session_uuid: str) -> str:
    """根据 session uuid 查询关联 persona 的 system_prompt"""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Session).where(Session.uid == uuid.UUID(session_uuid))
        )
        session = result.scalar_one_or_none()
        if not session:
            return "你是一位友好的对话伙伴。"

        if session.persona_id:
            result = await db.execute(
                select(Persona).where(Persona.id == session.persona_id)
            )
            persona = result.scalar_one_or_none()
            if persona:
                return persona.system_prompt

        return "你是一位友好的对话伙伴。"


@router.websocket("/sessions/{session_uuid}/ws")
async def websocket_voice_session(websocket: WebSocket, session_uuid: str):
    """
    对练会话 WebSocket 端点

    前端连接后，Pipeline 自动启动：
    - 接收：前端发送的 PCM 音频帧（protobuf 编码）
    - 发送：转录文本 + TTS 音频帧（protobuf 编码）
    """
    await websocket.accept()

    try:
        system_prompt = await _get_system_prompt(session_uuid)
        aiohttp_session = websocket.app.state.aiohttp_session
        await build_and_run_pipeline(websocket, system_prompt, aiohttp_session)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
