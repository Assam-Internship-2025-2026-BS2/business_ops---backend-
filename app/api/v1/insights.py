from fastapi import APIRouter, Query
from datetime import date
from app.services.insight_service import InsightService

router = APIRouter(tags=["Insights"])


@router.get("/insights")
def get_insights(metric_date: date = Query(...)):
    return InsightService.compute_insights(metric_date)