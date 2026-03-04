from datetime import date
from typing import List

from app.repositories.metrics_repository import MetricsRepository
from app.constants.thresholds import (
    CONVERSION_DROP_THRESHOLD,
    FAILURE_SPIKE_THRESHOLD,
    SLA_HOURS_THRESHOLD,
)
from app.schemas.insight_schema import InsightResponse, InsightCard


class InsightService:

    @staticmethod
    def compute_insights(metric_date: date) -> InsightResponse:

        today_data = MetricsRepository.get_today_metrics(metric_date)
        baseline_data = MetricsRepository.get_baseline_metrics(metric_date)

        insights: List[InsightCard] = []

        if not today_data or not baseline_data:
            return InsightResponse(
                date=str(metric_date),
                critical_count=0,
                insights=[]
            )

        today_conversion = today_data["conversion_rate"]
        today_failures = today_data["failed_transactions"]

        baseline_conversion = baseline_data["avg_conversion_rate"]
        baseline_failures = baseline_data["avg_failed_transactions"]

        # AC1 — Conversion Drop
    
        if baseline_conversion > 0:
            drop_percent = round(
                ((baseline_conversion - today_conversion) / baseline_conversion) * 100,
                2,
            )

            if drop_percent > (CONVERSION_DROP_THRESHOLD * 100):

                if drop_percent > 40:
                    severity = "CRITICAL"
                elif drop_percent > 25:
                    severity = "HIGH"
                else:
                    severity = "MEDIUM"

                insights.append(
                    InsightCard(
                        product="Payments",
                        type="Conversion Drop",  
                        severity=severity,
                        metric_value=drop_percent,
                        metric_unit="%",
                        stage="Checkout",
                        impact="Revenue Impacted",
                        message=f"Conversion dropped by {drop_percent}%",
                        cta_label="View Details",
                    )
                )

       
        # AC2 — Failure Spike
    
        if baseline_failures > 0:
            spike_percent = round(
                ((today_failures - baseline_failures) / baseline_failures) * 100,
                2,
            )

            if spike_percent > (FAILURE_SPIKE_THRESHOLD * 100):

                if spike_percent > 200:
                    severity = "CRITICAL"
                elif spike_percent > 100:
                    severity = "HIGH"
                else:
                    severity = "MEDIUM"

                insights.append(
                    InsightCard(
                        product="Payments",
                        type="Failure Spike",  
                        severity=severity,
                        metric_value=spike_percent,
                        metric_unit="%",
                        stage="Checkout",
                        impact="High failure rate",
                        message=f"Failures increased by {spike_percent}%",
                        cta_label="Explore Issue",
                    )
                )

        return InsightResponse(
            date=str(metric_date),
            critical_count=len(insights),
            insights=insights,
        )