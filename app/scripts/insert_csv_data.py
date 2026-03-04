from clickhouse_driver import Client
import pandas as pd

# Connect to ClickHouse
client = Client(
    host="localhost",
    port=9000,
    user="default",
    password="admin"
)

print("Connected to ClickHouse")

# ----------------------------
# Create Database
# ----------------------------

client.execute("""
CREATE DATABASE IF NOT EXISTS journey_dashboard
""")

print("Database created")


# ----------------------------
# Create Table
# ----------------------------

client.execute("""

CREATE TABLE IF NOT EXISTS journey_dashboard.journey_metrics
(

date Date,
channel String,
region String,
segment String,
product_name String,

started UInt32,
submitted UInt32,
in_progress UInt32,
completed UInt32,
approved UInt32,

failures UInt32,
avg_time_minutes UInt32,
sla_target_minutes UInt32,

pipeline_total_cr Float32,
pipeline_risk_cr Float32,

sla_breached UInt32,
stuck_24h UInt32

)

ENGINE = MergeTree()
ORDER BY (date, region, product_name)

""")

print("Table created")

# ----------------------------
# Load CSV
# ----------------------------

df = pd.read_csv("app/data/dashboard_data.csv")

df["date"] = pd.to_datetime(df["date"])

data = df.values.tolist()

# ----------------------------
# Insert Data
# ----------------------------

client.execute("""

INSERT INTO journey_dashboard.journey_metrics
VALUES

""", data)

print("Data inserted successfully")


# ----------------------------
# Test Query
# ----------------------------

result = client.execute("""

SELECT
product_name,
SUM(started),
SUM(submitted),
SUM(in_progress),
SUM(completed),
SUM(approved)

FROM journey_dashboard.journey_metrics

GROUP BY product_name

""")

print("\nQuery Result:\n")

for row in result:
    print(row)