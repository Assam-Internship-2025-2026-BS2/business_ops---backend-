def dashboard_query():
    return """
    SELECT
        lob AS category,
        segment AS product_name,
        COUNT(*) AS total_journeys,
        COUNTIf(status = 'SUCCESS') AS total_success,
        COUNTIf(status = 'ABANDONED') AS total_abandoned,
        COUNTIf(status = 'DROP_OFF_POLICY') AS drop_policy,
        COUNTIf(status = 'DROP_OFF_TECH') AS drop_tech
    FROM journey_instances
    WHERE is_valid = 1
    GROUP BY lob, segment
    """