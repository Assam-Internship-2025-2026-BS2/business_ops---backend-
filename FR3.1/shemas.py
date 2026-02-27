from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_journeys: int
    successful_journeys: int
    successful_percentage: float
    health_status: str