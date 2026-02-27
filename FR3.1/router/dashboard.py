from fastapi import APIRouter
from database import get_clickhouse_client
from dashboard_service import build_dashboard_response

router = APIRouter()


@router.get("/dashboard/overview")
def get_dashboard_overview():

    try:
        client = get_clickhouse_client()
        response = build_dashboard_response(client)
        client.close()
        return response

    except Exception:
        return {
            "overall_metrics": {
                "success_rate": 0,
                "abandonment_rate": 0,
                "dropoff_rate": 0
            },
            "products": [],
            "stage_matrix": [],
            "drop_reasons": {
                "abandoned": 0,
                "policy": 0,
                "tech": 0,
                "primary_driver": "Grey"
            }
        }