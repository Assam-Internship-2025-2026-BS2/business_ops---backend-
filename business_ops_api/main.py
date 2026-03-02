from fastapi import FastAPI
from services import fetch_dashboard_data
from schemas import DashboardResponse

app = FastAPI(
    title="Business Ops Dashboard API",
    version="2.0.0"
)

@app.get("/")
def home():
    return {"message": "Business Ops Dashboard API Running"}

@app.get("/dashboard", response_model=DashboardResponse)
def get_dashboard():
    return fetch_dashboard_data()