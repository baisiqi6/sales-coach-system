"""
CoachStage 应用配置
所有环境变量统一在此管理，读取 .env 文件。
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    应用配置类（Pydantic v2 Settings）
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ---- 应用基础配置 ----
    APP_NAME: str = "coach-stage"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ---- 数据库配置（独立字段，由 docker-compose 注入）----
    DB_USER: str = "coach_user"
    DB_PASSWORD: str = "change_me_in_production"
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "coach_stage"

    @property
    def DATABASE_URL(self) -> str:
        """异步 PostgreSQL 连接字符串（由独立字段拼接）"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # ---- Redis 配置 ----
    REDIS_PASSWORD: str = "change_me_in_production"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        """Redis 连接字符串（包含密码）"""
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # ---- 钉钉开放平台 ----
    DINGTALK_APP_KEY: str = ""
    DINGTALK_APP_SECRET: str = ""
    DINGTALK_CLIENT_ID: str = ""
    DINGTALK_CLIENT_SECRET: str = ""
    DINGTALK_STREAM_TOPIC: str = "/v1.0/im/bot/messages/get_by_app"

    # ---- LLM（OpenAI 兼容格式）----
    LLM_API_BASE: str = "https://api.deepseek.com/v1"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "deepseek-chat"

    # ---- ASR（阿里云语音识别）----
    ASR_APP_KEY: str = ""
    ASR_ACCESS_KEY_ID: str = ""
    ASR_ACCESS_KEY_SECRET: str = ""
    ASR_REGION: str = "cn-wulanchabu"

    # ---- TTS（MiniMax M2.7-highspeed）----
    TTS_API_KEY: str = ""
    TTS_MODEL: str = "MiniMax-M2.7-highspeed"
    TTS_VOICE_ID: str = ""

    # ---- 外部知识库 RAG ----
    RAG_API_URL: str = ""
    RAG_API_KEY: str = ""

    # ---- 跨域配置 ----
    CORS_ORIGINS: list[str] = ["*"]


# 全局单例，应用启动时实例化
settings = Settings()
