"""
Alembic 异步迁移环境配置

此文件在每次 alembic upgrade / revision 命令时加载，
负责：1) 从 app.core.config 读取 DATABASE_URL
      2) 创建异步 engine
      3) 执行迁移
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

# ---- 导入模型（必须，确保 Base.metadata 包含所有模型）----
from app.models import Base
from app.core.config import settings

# Alembic Config 对象
config = context.config

# ---- 动态注入 DATABASE_URL（alembic.ini 中 sqlalchemy.url 留空）----
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# ---- 启用 Alembic .ini 中的 logging 配置----
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ---- target_metadata 必须指向 Base.metadata ----
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    'offline' 模式：生成 SQL 脚本，不连接数据库
    alembic revision --autogenerate --sql 输出
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """
    同步包装器：async session 中通过 run_sync 调用同步迁移逻辑
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    'online' 模式：创建异步 engine，实时连接数据库执行迁移
    alembic upgrade head / alembic revision --autogenerate 使用此模式
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
