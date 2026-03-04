def executive_aggregate_query():
    return """
    SELECT
        SUM(started),
        SUM(submitted),
        SUM(in_progress),
        SUM(completed),
        SUM(approved),
        SUM(failures),

        AVG(avg_time_minutes),
        AVG(sla_target_minutes),

        SUM(pipeline_total_cr),
        SUM(pipeline_risk_cr),

        SUM(sla_breached),
        SUM(stuck_24h)
    FROM dashboard_data
    WHERE date BETWEEN %(from_date)s AND %(to_date)s
      AND (%(channel)s = 'All' OR channel = %(channel)s)
      AND (%(region)s = 'All' OR region = %(region)s)
      AND (%(segment)s = 'All' OR segment = %(segment)s)
    """


def max_product_time_query():
    return """
    SELECT product_name, MAX(avg_time_minutes)
    FROM dashboard_data
    WHERE date BETWEEN %(from_date)s AND %(to_date)s
    GROUP BY product_name
    ORDER BY MAX(avg_time_minutes) DESC
    LIMIT 1
    """


def product_alerts_query():
    return """
    SELECT
        product_name,
        SUM(started),
        SUM(completed),
        SUM(approved),
        SUM(failures),
        SUM(sla_breached)
    FROM dashboard_data
    WHERE date BETWEEN %(from_date)s AND %(to_date)s
      AND (%(channel)s = 'All' OR channel = %(channel)s)
      AND (%(region)s = 'All' OR region = %(region)s)
      AND (%(segment)s = 'All' OR segment = %(segment)s)
    GROUP BY product_name
    """