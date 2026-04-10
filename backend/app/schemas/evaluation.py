"""
评估报告 Schema
严格定义打分 JSON 格式，供前端雷达图和扣分点渲染使用
"""

from pydantic import BaseModel, ConfigDict


class EvaluationDimension(BaseModel):
    """
    单一评分维度
    如：沟通技巧、产品知识、异议处理、成交意识
    """
    name: str
    score: int          # 0-100
    max_score: int = 100
    weight: float = 1.0  # 权重，用于综合分计算
    comment: str | None = None  # 该维度的简短评价


class EvaluationReport(BaseModel):
    """
    综合评估报告（会话结束后生成）
    """
    total_score: int  # 综合评分 0-100
    dimensions: list[EvaluationDimension]  # 分维度评分列表
    strengths: list[str]  # 做得好的地方
    weaknesses: list[str]  # 扣分点/待改进
    suggestions: list[str]  # 改进建议
    summary: str  # 一句话总结


class EvaluationScore(BaseModel):
    """
    单轮对话即时评分（在 AI 回复后返回给前端）
    """
    message_uuid: str
    dimension_scores: list[EvaluationDimension]
    total_score: int  # 本轮综合分
