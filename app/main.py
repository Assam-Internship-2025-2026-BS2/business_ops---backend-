from fastapi import FastAPI
from app.api.v1.insights import router as insights_router
from app.routers.dashboard_router import router as dashboard_router

app = FastAPI(title="Journey Analytics API")

# Existing insights API
app.include_router(insights_router)

# Mamoni dashboard router
app.include_router(dashboard_router)