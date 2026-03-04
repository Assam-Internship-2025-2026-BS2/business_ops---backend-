from datetime import datetime, timedelta
from database import get_client
from queries import (
    executive_aggregate_query,
    max_product_time_query,
    product_alerts_query
)


def get_date_range(time_range):
    today = datetime.today().date()

    if time_range == "Today":
        return today, today
    elif time_range == "Yesterday":
        y = today - timedelta(days=1)
        return y, y
    elif time_range == "Last 7 Days":
        return today - timedelta(days=7), today
    elif time_range == "Last 30 Days":
        return today - timedelta(days=30), today
    else:
        return today.replace(day=1), today


def generate_alerts(client, params):

    alerts = []

    result = client.query(product_alerts_query(), parameters=params)
    rows = result.result_rows

    for row in rows:
        product = row[0]
        started = row[1] or 0
        completed = row[2] or 0
        approved = row[3] or 0
        failures = row[4] or 0
        sla_breached = row[5] or 0

        conversion = (completed / started) * 100 if started else 0

        if conversion < 40:
            alerts.append({
                "text": f"{product} conversion dropped below threshold ({round(conversion,1)}%)",
                "severity": "CRITICAL"
            })

        if failures > 50:
            alerts.append({
                "text": f"{product} failures increased significantly",
                "severity": "CRITICAL"
            })

        if sla_breached > 100:
            alerts.append({
                "text": f"{product} SLA breached — {sla_breached} cases",
                "severity": "WARNING"
            })

    return alerts


def fetch_executive_dashboard(time_range, channel, region, segment):

    client = get_client()

    from_date, to_date = get_date_range(time_range)

    params = {
        "from_date": from_date,
        "to_date": to_date,
        "channel": channel,
        "region": region,
        "segment": segment
    }

    result = client.query(executive_aggregate_query(), parameters=params)
    row = result.result_rows[0]

    started = row[0] or 0
    submitted = row[1] or 0
    in_progress = row[2] or 0
    completed = row[3] or 0
    approved = row[4] or 0
    failures = row[5] or 0
    avg_time = row[6] or 0
    sla_target = row[7] or 0
    pipeline_total = row[8] or 0
    pipeline_risk = row[9] or 0
    sla_breached = row[10] or 0
    stuck = row[11] or 0

    conversion = (completed / started) * 100 if started else 0
    approval = (approved / completed) * 100 if completed else 0
    pipeline_percentage = (pipeline_risk / pipeline_total) * 100 if pipeline_total else 0

    max_product_result = client.query(max_product_time_query(), parameters=params)
    max_product_row = max_product_result.result_rows[0] if max_product_result.result_rows else ["N/A", 0]

    alerts = generate_alerts(client, params)

    health_status = "WATCH" if len(alerts) > 0 else "STABLE"

    return {
        "overall_health": {
            "status": health_status,
            "critical_products": len(alerts),
            "message": f"{len(alerts)} products showing risk signals",
            "alerts": alerts
        },
        "kpi_cards": {
            "onboarding_started": {
                "value": started,
                "trend_percentage": 0,
                "trend_direction": "UP",
                "submitted": submitted,
                "in_progress": in_progress
            },
            "onboarding_completed": {
                "value": completed,
                "trend_percentage": 0,
                "trend_direction": "UP",
                "conversion_rate": round(conversion, 2),
                "approval_rate": round(approval, 2)
            },
            "avg_completion_time": {
                "value_minutes": round(avg_time, 2),
                "trend_minutes": 0,
                "trend_direction": "UP",
                "sla_target_minutes": round(sla_target, 2),
                "max_product_time_minutes": round(max_product_row[1], 2),
                "max_product_name": max_product_row[0]
            },
            "pipeline_at_risk": {
                "amount_cr": round(pipeline_risk, 2),
                "trend_cr": 0,
                "trend_direction": "UP",
                "percentage_of_total_pipeline": round(pipeline_percentage, 2),
                "sla_breached": sla_breached,
                "stuck_over_24h": stuck
            }
        },
        "filters_applied": {
            "time_range": time_range,
            "channel": channel,
            "region": region,
            "segment": segment
        },
        "data_as_of_timestamp": datetime.utcnow()
    }