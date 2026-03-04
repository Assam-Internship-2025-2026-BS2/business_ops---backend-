from fastapi import FastAPI
from app.routers.dashboard_router import router

app = FastAPI(title="Journey Analytics API")

app.include_router(router)