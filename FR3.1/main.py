from fastapi import FastAPI
from router import dashboard
from database import get_clickhouse_client

app = FastAPI(
    title="Business Ops Dashboard API",
    version="1.0.0"
)

app.include_router(dashboard.router)

@app.get("/health")
def health_check():
    return {"status": "API Running"}

@app.get("/test-db")
def test_db():
    try:
        client = get_clickhouse_client()
        result = client.query("SELECT count() FROM journeys")
        client.close()

        return {
            "database": "connected",
            "rows_in_journeys": result.result_rows
        }

    except Exception as e:
        return {
            "database": "failed",
            "error": str(e)
        }

@app.get("/debug-db")
def debug_db():
    client = get_clickhouse_client()

    version = client.query("SELECT version()").result_rows
    database = client.query("SELECT currentDatabase()").result_rows
    tables = client.query("SHOW TABLES").result_rows

    client.close()

    return {
        "version": version,
        "current_database": database,
        "tables": tables
    }