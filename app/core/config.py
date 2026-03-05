from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CLICKHOUSE_HOST: str = "localhost"
    CLICKHOUSE_PORT: int = 9000
    CLICKHOUSE_USER: str = "default"
    CLICKHOUSE_PASSWORD: str = "REstart@789"
    CLICKHOUSE_DB: str = "business_ops"

    class Config:
        env_file = ".env"


settings = Settings()