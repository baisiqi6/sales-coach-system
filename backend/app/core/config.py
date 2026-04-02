"""
应用配置
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""

    # 应用基础配置
    APP_NAME: str = "智能销售对练系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/sales_coach"

    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"

    # 钉钉配置
    DINGTALK_APP_KEY: str = ""
    DINGTALK_APP_SECRET: str = ""
    DINGTALK_CLIENT_ID: str = ""
    DINGTALK_CLIENT_SECRET: str = ""

    # LLM 配置 (OpenAI 兼容格式)
    LLM_API_BASE: str = "https://api.openai.com/v1"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"

    # ASR 配置 (阿里云)
    ASR_APP_KEY: str = ""
    ASR_ACCESS_KEY_ID: str = ""
    ASR_ACCESS_KEY_SECRET: str = ""

    # 跨域配置
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
