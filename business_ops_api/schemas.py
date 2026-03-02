from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    product_name: str
    successful: int
    abandoned: int
    drop_off_policy: int
    drop_off_tech: int
    health_status: str


class Category(BaseModel):
    category: str
    products: List[Product]


class AlertProduct(BaseModel):
    product: str
    success_rate: int
    status: str


class OverallHealth(BaseModel):
    status: str
    red_products: int
    amber_products: int
    alerts: List[AlertProduct]


class SummaryMetrics(BaseModel):
    overall_success_rate: int
    customer_abandonment_rate: int
    total_drop_off_rate: int
    active_products_monitored: int
    green_products: int
    red_products: int


class DashboardResponse(BaseModel):
    overall_health: OverallHealth
    summary_metrics: SummaryMetrics
    journey_performance_by_category: List[Category]