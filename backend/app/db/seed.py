"""
数据库种子数据

创建测试用户和 AI 分身角色，用于 MVP 开发和测试。
"""

import asyncio
import uuid

from sqlalchemy import select

from app.core.database import async_engine, AsyncSessionLocal
from app.models.user import User
from app.models.persona import Persona

# 测试用户
TEST_USERS = [
    {
        "dingtalk_userid": "test_sale_001",
        "name": "张三（测试销售）",
        "role": "SALE",
    },
    {
        "dingtalk_userid": "test_manager_001",
        "name": "李经理（测试主管）",
        "role": "MANAGER",
    },
]

# 测试 AI 分身
TEST_PERSONAS = [
    {
        "name": "价格异议客户",
        "scenario_desc": "客户对价格非常敏感，总是质疑报价合理性，会对比竞品价格并试图压价",
        "system_prompt": (
            "你是一位对价格非常敏感的客户，正在与一位销售代表交谈。"
            "你总是质疑价格是否合理，会比较竞品价格，并试图压价。"
            "你的语气要自然，像真实客户一样，有时犹豫，有时坚持。"
            "请用中文回应，每次回复1-2句话，保持对话自然流畅。"
        ),
    },
    {
        "name": "产品咨询客户",
        "scenario_desc": "客户对产品功能很感兴趣，但有很多技术细节问题需要确认",
        "system_prompt": (
            "你是一位对产品功能很感兴趣的潜在客户，正在与销售代表交谈。"
            "你会提出很多技术细节问题，比如性能指标、兼容性、售后保障等。"
            "你态度友好但谨慎，不会轻易做决定，需要充分了解后才考虑购买。"
            "请用中文回应，每次回复1-2句话，保持对话自然流畅。"
        ),
    },
    {
        "name": "成交犹豫客户",
        "scenario_desc": "客户已经基本认可产品，但在签约环节犹豫不决，需要销售促成",
        "system_prompt": (
            "你是一位已经基本认可产品的客户，正在与销售代表交谈。"
            "你在签约环节犹豫不决，会提出各种顾虑：预算审批时间、合同条款、实施风险等。"
            "你内心想买但需要销售给你足够的信心和推动力。"
            "请用中文回应，每次回复1-2句话，保持对话自然流畅。"
        ),
    },
]


async def seed():
    """写入种子数据"""
    async with AsyncSessionLocal() as db:
        # 创建测试用户
        for user_data in TEST_USERS:
            result = await db.execute(
                select(User).where(User.dingtalk_userid == user_data["dingtalk_userid"])
            )
            if result.scalar_one_or_none():
                continue
            user = User(**user_data)
            db.add(user)

        await db.flush()

        # 获取主管用户 ID
        result = await db.execute(
            select(User).where(User.dingtalk_userid == "test_manager_001")
        )
        manager = result.scalar_one_or_none()

        # 创建测试分身
        for persona_data in TEST_PERSONAS:
            result = await db.execute(
                select(Persona).where(Persona.name == persona_data["name"])
            )
            if result.scalar_one_or_none():
                continue
            persona = Persona(
                **persona_data,
                created_by_manager_id=manager.id if manager else None,
            )
            db.add(persona)

        await db.commit()

    await async_engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
