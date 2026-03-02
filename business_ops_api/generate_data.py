import random
from datetime import date, timedelta
import clickhouse_connect

client = clickhouse_connect.get_client(
    host="localhost",
    port=8123,
    username="default",
    password="REstart@789",
    database="business_ops"
)


channels = ["Mobile App", "Net Banking", "Branch"]
regions = ["North Zone", "South Zone", "East Zone", "West Zone"]
segments = ["Retail", "Priority", "SME"]
products = ["Credit Card", "Personal Loan", "Home Loan"]

start_date = date(2026, 2, 1)
days = 30


rows = []

for i in range(days):
    current_date = start_date + timedelta(days=i)

    for channel in channels:
        for region in regions:
            for segment in segments:
                for product in products:

                    started = random.randint(800, 2000)
                    submitted = int(started * random.uniform(0.5, 0.8))
                    in_progress = started - submitted
                    completed = int(started * random.uniform(0.4, 0.7))
                    approved = int(completed * random.uniform(0.6, 0.9))
                    failures = random.randint(10, 120)

                    avg_time = random.randint(15, 45)
                    sla_target = random.choice([15, 20, 25])

                    pipeline_total = random.randint(15, 40)
                    pipeline_risk = round(pipeline_total * random.uniform(0.05, 0.3), 2)

                    sla_breached = random.randint(20, 200)
                    stuck_24h = random.randint(5, 120)

                    rows.append((
                        current_date,
                        channel,
                        region,
                        segment,
                        product,
                        started,
                        submitted,
                        in_progress,
                        completed,
                        approved,
                        failures,
                        avg_time,
                        sla_target,
                        pipeline_total,
                        pipeline_risk,
                        sla_breached,
                        stuck_24h
                    ))


client.insert(
    "dashboard_data",
    rows,
    column_names=[
        "date",
        "channel",
        "region",
        "segment",
        "product_name",
        "started",
        "submitted",
        "in_progress",
        "completed",
        "approved",
        "failures",
        "avg_time_minutes",
        "sla_target_minutes",
        "pipeline_total_cr",
        "pipeline_risk_cr",
        "sla_breached",
        "stuck_24h"
    ]
)

print(f"Inserted {len(rows)} rows successfully.")