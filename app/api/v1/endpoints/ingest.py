from chromadb.api import ClientAPI
import logging
import itertools
from typing import Any
from fastapi import APIRouter, status, Depends, BackgroundTasks
from app.core.deps import get_chroma_db
from app.repositories.telemetry import TelemetryRepository
from app.schemas.telemetry import TelemetryPayload
from app.schemas.ingest import IngestResponse

request_counter = itertools.count(start=1)
logger = logging.getLogger(__name__)
router = APIRouter()

def store_telemetry(db: ClientAPI, node_id: str, payload: TelemetryPayload):
    """ Background task: Performs the actual ChromaDB upsert with a write lock.
    """
    import json

     # Fast: Grabs the collection instantly because it was guaranteed at server boot
    collection = db.get_collection(name="industrial_telemetry_store")
    telemetry_repo = TelemetryRepository(collection)

    flat_metadata = {
        "node_id": node_id,
        "timestamp": payload.timestamp.isoformat(),
        "metric_type": payload.metric_type,
        "status_code": str(payload.status_code),
        "structured_metrics.json": json.dumps(payload.structured_metrics)
    }
    telemetry_repo.store_without_lock(
        ids=[f"{node_id}_{payload.timestamp.timestamp()}"],
        documents=[payload.data_summary],
        metadatas=[flat_metadata],
    )
    logger.info(f"Telemetry packet committed cleanly to disk storage for node {node_id} at {payload.timestamp.isoformat()}.")
    

@router.get("/nodes", response_model=dict[str, Any])
def get_active_nodes() -> dict[str, Any]:
    return {"message": "You have reached the nodes endpoint", "status_code": status.HTTP_200_OK}

@router.post("/nodes/{node_id}/ingest", response_model=IngestResponse)
def log_data(
    node_id: str,
    payload: TelemetryPayload,
    background_tasks: BackgroundTasks,
    db: ClientAPI = Depends(get_chroma_db)
) -> IngestResponse:
    count = next(request_counter)
    # Validate the node_id in URL matches body (if present)
    if payload.node_id != node_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=422, detail="node_id mismatch")
    
    # Schedule the actual storage as a background task
    background_tasks.add_task(store_telemetry, db, node_id, payload)

    logger.info(f"Telemetry packet accepted for node {node_id} at {payload.timestamp.isoformat()}.")
    return IngestResponse(
        status_code= status.HTTP_202_ACCEPTED,
        node_id=node_id,
        processed_records=f"1 record processed for node {node_id} at {payload.timestamp.isoformat()}",
        message=f"{count} Telemetry packet committed cleanly to disk storage."
    )
    