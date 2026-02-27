from dashboard_repository import (
    fetch_overall_metrics,
    fetch_product_metrics,
    fetch_stage_matrix
)


def calculate_status(success_rate):

    if success_rate >= 50:
        return "Green"
    elif success_rate >= 35:
        return "Amber"
    elif success_rate > 0:
        return "Red"
    return "Grey"


def build_dashboard_response(client):

    overall = fetch_overall_metrics(client)
    total = overall["total"]

    if total == 0:
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
                "primary_driver": "No Data"
            }
        }

  
    success_rate = round((overall["success"] / total) * 100, 2)
    abandonment_rate = round((overall["abandoned"] / total) * 100, 2)
    dropoff_rate = round(
        ((overall["policy_drop"] + overall["tech_drop"]) / total) * 100, 2
    )

    product_rows = fetch_product_metrics(client)
    products = []

    for row in product_rows:
        product, total_p, success, abandoned, policy, tech = row

        if total_p == 0:
            continue

        success_pct = round((success / total_p) * 100, 2)

        products.append({
            "name": product,
            "successful": success_pct,
            "abandoned": round((abandoned / total_p) * 100, 2),
            "dropoff_policy": round((policy / total_p) * 100, 2),
            "dropoff_tech": round((tech / total_p) * 100, 2),
            "status": calculate_status(success_pct)
        })

    stage_rows = fetch_stage_matrix(client)
    stage_matrix = []

    for row in stage_rows:
        stage, total_s, progressed, policy, tech, abandoned = row

        stage_matrix.append({
            "stage": stage,
            "total_reached": total_s,
            "progressed": progressed,
            "dropoff_policy": policy,
            "dropoff_tech": tech,
            "abandoned": abandoned
        })

    drop_reasons = {
        "abandoned": abandonment_rate,
        "policy": round((overall["policy_drop"] / total) * 100, 2),
        "tech": round((overall["tech_drop"] / total) * 100, 2),
        "primary_driver": "Customer exited voluntarily"
    }

    return {
        "overall_metrics": {
            "success_rate": success_rate,
            "abandonment_rate": abandonment_rate,
            "dropoff_rate": dropoff_rate
        },
        "products": products,
        "stage_matrix": stage_matrix,
        "drop_reasons": drop_reasons
    }