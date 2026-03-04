from fastapi import FastAPI
<<<<<<< HEAD
from app.api.v1.insights import router as insights_router

app = FastAPI(
    title="Today Key Insights API",
    description="Backend service for computing business critical alerts (FR5.3)",
    version="1.0.0"
)

app.include_router(insights_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "OK"}
=======
from app.routers.dashboard_router import router

app = FastAPI(title="Journey Analytics API")

app.include_router(router)
>>>>>>> origin/Mamoni-Sheikh
