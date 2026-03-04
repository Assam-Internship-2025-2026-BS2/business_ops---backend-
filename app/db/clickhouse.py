from clickhouse_driver import Client
from app.core.config import settings


class ClickHouseConnection:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = Client(
                host=settings.CLICKHOUSE_HOST,
                port=settings.CLICKHOUSE_PORT,
                database=settings.CLICKHOUSE_DB,
                user=settings.CLICKHOUSE_USER,
                password=settings.CLICKHOUSE_PASSWORD,
            )
        return cls._client