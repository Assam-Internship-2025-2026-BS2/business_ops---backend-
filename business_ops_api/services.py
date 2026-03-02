from database import get_client
from queries import dashboard_query


def calculate_health(success_rate):
    if success_rate >= 60:
        return "GREEN"
    elif success_rate >= 40:
        return "AMBER"
    else:
        return "RED"


def fetch_dashboard_data():
    client = get_client()
    query = dashboard_query()
    result = client.query(query)

    rows = result.result_rows

    categories = {}
    total_success = 0
    total_journeys = 0
    total_abandoned = 0
    total_drop_policy = 0
    total_drop_tech = 0

    red_count = 0
    amber_count = 0
    green_count = 0
    alerts = []

    for row in rows:
        category = row[0]
        product_name = row[1]
        total = row[2]
        success = row[3]
        abandoned = row[4]
        drop_policy = row[5]
        drop_tech = row[6]

        if total == 0:
            continue

        success_rate = round((success / total) * 100)
        abandoned_rate = round((abandoned / total) * 100)
        drop_policy_rate = round((drop_policy / total) * 100)
        drop_tech_rate = round((drop_tech / total) * 100)

        health = calculate_health(success_rate)

        if health == "RED":
            red_count += 1
            alerts.append({
                "product": product_name,
                "success_rate": success_rate,
                "status": "RED"
            })
        elif health == "AMBER":
            amber_count += 1
        else:
            green_count += 1

        if category not in categories:
            categories[category] = []

        categories[category].append({
            "product_name": product_name,
            "successful": success_rate,
            "abandoned": abandoned_rate,
            "drop_off_policy": drop_policy_rate,
            "drop_off_tech": drop_tech_rate,
            "health_status": health
        })

        total_success += success
        total_journeys += total
        total_abandoned += abandoned
        total_drop_policy += drop_policy
        total_drop_tech += drop_tech

    overall_success_rate = round((total_success / total_journeys) * 100)
    customer_abandonment_rate = round((total_abandoned / total_journeys) * 100)
    total_drop_off_rate = round(((total_drop_policy + total_drop_tech) / total_journeys) * 100)

    overall_status = "WATCH" if red_count > 0 else "STABLE"

    return {
        "overall_health": {
            "status": overall_status,
            "red_products": red_count,
            "amber_products": amber_count,
            "alerts": alerts
        },
        "summary_metrics": {
            "overall_success_rate": overall_success_rate,
            "customer_abandonment_rate": customer_abandonment_rate,
            "total_drop_off_rate": total_drop_off_rate,
            "active_products_monitored": len(rows),
            "green_products": green_count,
            "red_products": red_count
        },
        "journey_performance_by_category": [
            {
                "category": cat,
                "products": products
            }
            for cat, products in categories.items()
        ]
    }