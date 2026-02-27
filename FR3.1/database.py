import clickhouse_connect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_clickhouse_client():
    try:
        client = clickhouse_connect.get_client(
            host="localhost",
            port=8123,
            username="default",
            password="",
            database="default"
        )


        client.query("SELECT 1")
        logger.info("ClickHouse Connected Successfully")

        return client

    except Exception as e:
        logger.error(f"ClickHouse connection failed: {e}")
        raise Exception("Database connection failed")