"""
Pipecat 实时语音 Pipeline

构建 STT(faster-whisper) → LLM(DeepSeek) → TTS(MiniMax) 的实时语音对话 Pipeline，
通过 FastAPI WebSocket 与前端通信。
"""

import aiohttp
from fastapi import WebSocket

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import EndFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.serializers.protobuf import ProtobufFrameSerializer
from pipecat.services.deepseek.llm import DeepSeekLLMService
from pipecat.services.minimax.tts import MiniMaxHttpTTSService
from pipecat.services.whisper.stt import WhisperSTTService, Model
from pipecat.transcriptions.language import Language
from pipecat.transports.websocket.fastapi import (
    FastAPIWebsocketTransport,
    FastAPIWebsocketParams,
)

from app.core.config import settings


def _build_stt() -> WhisperSTTService:
    """构建本地 faster-whisper STT 服务"""
    model_map = {
        "tiny": Model.TINY,
        "base": Model.BASE,
        "small": Model.SMALL,
        "medium": Model.MEDIUM,
        "large": Model.LARGE,
        "large-v3-turbo": Model.LARGE_V3_TURBO,
        "distil-large-v2": Model.DISTIL_LARGE_V2,
    }
    return WhisperSTTService(
        model=model_map.get(settings.WHISPER_MODEL, Model.LARGE_V3_TURBO),
        device=settings.WHISPER_DEVICE,
        compute_type=settings.WHISPER_COMPUTE_TYPE,
    )


def _build_llm(system_prompt: str) -> DeepSeekLLMService:
    """构建 DeepSeek LLM 服务"""
    return DeepSeekLLMService(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_API_BASE,
        settings=DeepSeekLLMService.Settings(
            model=settings.LLM_MODEL,
            system_instruction=system_prompt,
            temperature=0.7,
            max_tokens=256,
        ),
    )


def _build_tts(aiohttp_session: aiohttp.ClientSession) -> MiniMaxHttpTTSService:
    """构建 MiniMax TTS 服务"""
    return MiniMaxHttpTTSService(
        api_key=settings.TTS_API_KEY,
        group_id=settings.MINIMAX_GROUP_ID,
        aiohttp_session=aiohttp_session,
        settings=MiniMaxHttpTTSService.Settings(
            model=settings.TTS_MODEL,
            voice=settings.MINIMAX_VOICE,
            language=Language.ZH,
            speed=1.0,
        ),
    )


async def build_and_run_pipeline(
    websocket: WebSocket,
    system_prompt: str,
    aiohttp_session: aiohttp.ClientSession,
) -> None:
    """
    构建并运行 Pipecat Pipeline，阻塞直到会话结束。

    Args:
        websocket: FastAPI WebSocket 连接
        system_prompt: AI 分身的系统提示词
        aiohttp_session: 共享的 aiohttp 会话（MiniMax TTS 需要）
    """
    # 1. Transport
    transport = FastAPIWebsocketTransport(
        websocket,
        params=FastAPIWebsocketParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            add_wav_header=False,
            serializer=ProtobufFrameSerializer(),
        ),
    )

    # 2. AI Services
    stt = _build_stt()
    llm = _build_llm(system_prompt)
    tts = _build_tts(aiohttp_session)

    # 3. VAD + Context Aggregators
    context = LLMContext()
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(
            vad_analyzer=SileroVADAnalyzer(
                params=SileroVADAnalyzer.Params(
                    stop_secs=0.8,  # 中文语速有停顿，避免过早截断
                ),
            ),
        ),
    )

    # 4. Pipeline
    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            user_aggregator,
            llm,
            tts,
            transport.output(),
            assistant_aggregator,
        ]
    )

    # 5. Task + Runner
    task = PipelineTask(pipeline, params=PipelineParams(enable_metrics=True))

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, ws):
        pass

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, ws):
        await task.queue_frame(EndFrame())

    runner = PipelineRunner()
    await runner.run(task)
