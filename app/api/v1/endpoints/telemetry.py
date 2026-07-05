import asyncio
import logging
from app.schemas.telemetry import PayloadTelemetry
from fastapi import APIRouter, status

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/telemetry", status_code=status.HTTP_201_CREATED)
async def log_machine_state(state: PayloadTelemetry):
    asyncio.sleep(0.5)
