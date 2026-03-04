from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from services import fetch_executive_dashboard
from schemas import ExecutiveResponse

app = FastAPI(
    title="Business Ops Executive API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Business Ops Executive API is running",
    }


@app.get("/executive-dashboard", response_model=ExecutiveResponse)
def get_executive_dashboard(
    time_range: str = Query("This Month"),
    channel: str = Query("All"),
    region: str = Query("All"),
    segment: str = Query("All"),
    comparison: str = Query("V/S Last Month")
):
    try:
        data = fetch_executive_dashboard(
            time_range=time_range,
            channel=channel,
            region=region,
            segment=segment
        )
        return data

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": str(e)
            }
        )