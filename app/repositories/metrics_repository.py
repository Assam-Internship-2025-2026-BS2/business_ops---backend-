from datetime import date
from app.core.database import get_clickhouse_client

class MetricsRepository:

    @staticmethod
    def get_today_metrics(metric_date: date):
        result = get_clickhouse_client().execute(
            """
            SELECT conversion_rate, failed_transactions
            FROM daily_metrics
            WHERE metric_date = %(metric_date)s
            """,
            {"metric_date": metric_date}
        )

        if not result:
            return None

        conversion_rate, failed_transactions = result[0]
        return {"conversion_rate": float(conversion_rate), "failed_transactions": int(failed_transactions)}

    @staticmethod
    def get_baseline_metrics(metric_date: date):
        result = get_clickhouse_client().execute(
            """
            SELECT 
                avg(conversion_rate), 
                avg(failed_transactions)
            FROM daily_metrics
            WHERE metric_date < %(metric_date)s
            """,
            {"metric_date": metric_date}
        )

        if not result or result[0][0] is None:
            return None

        avg_conversion, avg_failed = result[0]
        return {"avg_conversion_rate": float(avg_conversion), "avg_failed_transactions": float(avg_failed)}