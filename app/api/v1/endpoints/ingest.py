from chromadb.api import ClientAPI
import logging
from typing import Any
from fastapi import APIRouter, status, Depends
from app.core.deps import get_chroma_db
from app.schemas.telemetry import TelemetryPayload
from app.schemas.ingest import IngestResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/nodes", response_model=dict[str, Any])
def get_active_nodes() -> dict[str, Any]:
    return {"message": "You have reached the nodes endpoint", "status_code": status.HTTP_200_OK}

@router.post("/nodes/{node_id}/ingest", response_model=IngestResponse)
def log_data(node_id: str, payload: TelemetryPayload, db: ClientAPI = Depends(get_chroma_db)) -> IngestResponse:
    # Fast: Grabs the collection instantly because it was guaranteed at server boot
    collection = db.get_collection(name="industrial_telemetry_store")

    collection.upsert(
        ids=[f"{node_id}_{payload.timestamp.timestamp()}"],
        documents=[payload.data_summary],
        metadatas=[payload.structured_metrics],
    )
    logger.info(f"Telemetry packet committed cleanly to disk storage for node {node_id} at {payload.timestamp.isoformat()}.")
    return IngestResponse(
        status_code= status.HTTP_201_CREATED,
        node_id=node_id,
        processed_records=f"1 record processed for node {node_id} at {payload.timestamp.isoformat()}",
        message="Telemetry packet committed cleanly to disk storage."
    )
    