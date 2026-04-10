"""
对练会话核心接口

包含：创建会话、发送消息（SSE流式响应）、结束会话
这是系统的核心业务流，涉及：
- ASR（语音转文字）
- LLM（流式对话）
- TTS（文字转语音 + SSE推送）
- 实时评估
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.session import SessionCreate, SessionResponse, SessionEndRequest

router = APIRouter(prefix="/sessions", tags=["对练会话"])


@router.post("", response_model=SessionResponse, status_code=201)
async def create_session(
    payload: SessionCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    创建对练会话

    前端选择分身后调用此接口创建会话，
    返回会话 uuid 用于后续的消息收发
    """
    # TODO: INSERT INTO sessions ...
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="创建会话功能待实现",
    )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """
    获取会话详情
    """
    # TODO: SELECT * FROM sessions WHERE id = session_id
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="获取会话详情待实现",
    )


@router.post("/{session_id}/message")
async def send_message(
    session_id: int,
    # 前端上传录音文件（MP3），也可以传文本（调试用）
    audio: UploadFile = File(...),
    text: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    发送消息并获取 AI 回复（核心接口）

    数据流：
    1. 接收前端上传的录音文件（或文本）
    2. ASR（Whisper）将音频转为文本
    3. LLM 根据上下文生成回复（流式）
    4. TTS 将回复文本转为音频
    5. SSE 推送 TTS 音频流给前端，同时流式推送文本 chunks
    6. 实时评估本轮对话

    返回格式：SSE 流，包含：
      - event: text      data: {"content": "回复文本片段", "done": false}
      - event: audio_url data: {"url": "https://..."}
      - event: score     data: {"dimension_scores": [...], "total_score": 85}
      - event: done      data: {}

    注意：Cache-Control: no-cache，防止前端 SSE 不更新
    """
    # TODO: ASR → LLM → TTS → SSE Push + 评估
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="对练消息流待实现",
    )


@router.post("/{session_id}/end", response_model=SessionResponse)
async def end_session(
    session_id: int,
    payload: SessionEndRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    结束对练，生成综合评估报告

    将 session.status 改为 COMPLETED，
    生成 report_json 并写入 score_detail_json
    """
    # TODO: UPDATE sessions SET status=COMPLETED, report_json=... WHERE id=session_id
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="结束对练功能待实现",
    )
