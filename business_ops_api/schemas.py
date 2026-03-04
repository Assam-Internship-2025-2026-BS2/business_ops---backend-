from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime


class Alert(BaseModel):
    text: str
    severity: str


class ExecutiveResponse(BaseModel):
    overall_health: Dict
    kpi_cards: Dict
    filters_applied: Dict
    data_as_of_timestamp: datetime