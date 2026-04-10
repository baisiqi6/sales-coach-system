"""
SQLAlchemy 2.0 异步数据库引擎和会话管理
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from typing import AsyncGenerator

from app.core.config import settings

# ---- 异步引擎 ----
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # 开发环境打印 SQL，方便调试
    pool_size=10,         # 常驻连接数
    max_overflow=20,     # 超出 pool_size 的额外连接数上限
    pool_pre_ping=True,  # 每次从池中取连接前先 ping，避免断开的连接
)

# ---- 异步会话工厂 ----
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 提交后不自动过期，懒加载字段仍可访问
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI 依赖注入：每次请求创建一个独立的异步会话，请求结束后自动关闭。
    用法：
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
