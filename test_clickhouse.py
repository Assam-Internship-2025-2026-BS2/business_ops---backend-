from clickhouse_driver import Client

client = Client(
    host='localhost',
    port=9000,
    user='default',
    password='REstart@789',
    database='business_ops'
)

result = client.execute("SELECT metric_date, conversion_rate FROM daily_metrics")
print(result)