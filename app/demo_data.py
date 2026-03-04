import random
from datetime import datetime, timedelta
from clickhouse_driver import Client
import os
from dotenv import load_dotenv

load_dotenv()

client = Client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    port=int(os.getenv("CLICKHOUSE_PORT", 9000)),
    user=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", ""),
    database=os.getenv("CLICKHOUSE_DB", "default"),
)

TABLE_NAME = "transactions"

today = datetime(2026, 3, 4)

def insert_row(row):
    client.execute(
        f"""
        INSERT INTO {TABLE_NAME}
        (event_date, product, stage, device, zone, status, error_type, processing_time, revenue, user_id)
        VALUES
        """,
        [row],
    )

def generate_baseline():
    print("🔹 Inserting 7-day good baseline data...")

    for i in range(1, 8):
        day = today - timedelta(days=i)

        for _ in range(300):
            insert_row((
                day.date(),
                "Credit Card",
                "Video KYC",
                "Android",
                "West",
                "success" if random.random() < 0.80 else "failure",
                "timeout",
                random.randint(100, 500),
                5000,
                f"user_base_{random.randint(1,100000)}"
            ))

    print("Baseline data inserted")


def generate_bad_today():
    print("🔹 Inserting bad data for today...")

    for _ in range(400):
        insert_row((
            today.date(),
            "Credit Card",
            "Video KYC",
            "Android",
            "West",
            "success" if random.random() < 0.55 else "failure",  
            "agent_unavailable",
            random.randint(8000, 12000), 
            5000,
            f"user_today_{random.randint(1,100000)}"
        ))

    print(" Bad today data inserted")


if __name__ == "__main__":
    generate_baseline()
    generate_bad_today()
    print(" Demo data generation completed.")