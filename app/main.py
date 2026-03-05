from fastapi import FastAPI
from app.api.v1.insights import router as insights_router
from app.routers.dashboard_router import router as dashboard_router

app = FastAPI(
    title="Journey Analytics API",
    description="Backend service for computing business insights and dashboard analytics",
    version="1.0.0"
)

app.include_router(insights_router, prefix="/api/v1")

app.include_router(dashboard_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "OK"}