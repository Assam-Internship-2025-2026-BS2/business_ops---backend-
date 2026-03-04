from fastapi import APIRouter, Query
from app.services.stage_dropoff_service import get_stage_dropoff
from typing import List, Dict

router = APIRouter()


@router.get("/dashboard/stage-dropoff", response_model=List[Dict])
def stage_dropoff(
    channel: str = Query(None),
    region: str = Query(None),
    segment: str = Query(None)
):

    filters = {
        "channel": channel,
        "region": region,
        "segment": segment
    }

    data = get_stage_dropoff(filters)

    return data