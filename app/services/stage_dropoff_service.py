from app.database.clickhouse_client import client
from app.utils.calculations import calculate_dropoff


def get_stage_dropoff(filters):

    conditions = []
    params = {}

    if filters.get("channel"):
        conditions.append("channel = %(channel)s")
        params["channel"] = filters["channel"]

    if filters.get("region"):
        conditions.append("region = %(region)s")
        params["region"] = filters["region"]

    if filters.get("segment"):
        conditions.append("segment = %(segment)s")
        params["segment"] = filters["segment"]

    where = ""

    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    query = f"""
    SELECT
        product_name,
        SUM(started) AS started,
        SUM(submitted) AS submitted,
        SUM(in_progress) AS in_progress,
        SUM(completed) AS completed,
        SUM(approved) AS approved

    FROM journey_metrics
    {where}

    GROUP BY product_name
    """

    result = client.execute(query, params)

    response = []

    for row in result:

        product = row[0]

        started = row[1]
        submitted = row[2]
        progress = row[3]
        completed = row[4]
        approved = row[5]

        response.append({
            "product": product,
            "OTP Verify": calculate_dropoff(started, submitted),
            "CKYC/KYC": calculate_dropoff(submitted, progress),
            "Doc Upload": calculate_dropoff(progress, completed),
            "Eligibility": calculate_dropoff(completed, approved)
        })

    return response