def fetch_overall_metrics(client):

    query = """
        SELECT
            count() as total,
            countIf(status = 'SUCCESS') as success,
            countIf(status = 'ABANDONED') as abandoned,
            countIf(status = 'POLICY_DROP') as policy_drop,
            countIf(status = 'TECH_DROP') as tech_drop
        FROM journeys
    """

    try:
        result = client.query(query)
        row = result.result_rows[0]

        return {
            "total": row[0],
            "success": row[1],
            "abandoned": row[2],
            "policy_drop": row[3],
            "tech_drop": row[4]
        }

    except Exception:
        return {
            "total": 0,
            "success": 0,
            "abandoned": 0,
            "policy_drop": 0,
            "tech_drop": 0
        }


def fetch_product_metrics(client):

    query = """
        SELECT
            product,
            count() as total,
            countIf(status='SUCCESS') as success,
            countIf(status='ABANDONED') as abandoned,
            countIf(status='POLICY_DROP') as policy_drop,
            countIf(status='TECH_DROP') as tech_drop
        FROM journeys
        GROUP BY product
    """

    try:
        result = client.query(query)
        return result.result_rows
    except Exception:
        return []


def fetch_stage_matrix(client):

    query = """
        SELECT
            stage,
            count() as total,
            countIf(status='SUCCESS') as progressed,
            countIf(status='POLICY_DROP') as policy_drop,
            countIf(status='TECH_DROP') as tech_drop,
            countIf(status='ABANDONED') as abandoned
        FROM journeys
        GROUP BY stage
    """

    try:
        result = client.query(query)
        return result.result_rows
    except Exception:
        return []