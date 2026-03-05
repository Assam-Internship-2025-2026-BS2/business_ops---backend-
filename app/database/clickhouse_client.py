from clickhouse_driver import Client

client = Client(
    host="localhost",
    port=9000,
    user="default",
    password="REstart@789",
    database="business_ops"
)

def get_clickhouse_client():
    return client