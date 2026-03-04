from pydantic import BaseModel
from typing import List


class InsightCard(BaseModel):
    product: str
    type: str
    severity: str
    metric_value: float
    metric_unit: str
    stage: str
    impact: str
    message: str
    cta_label: str


class InsightResponse(BaseModel):
    date: str
    critical_count: int
    insights: List[InsightCard]