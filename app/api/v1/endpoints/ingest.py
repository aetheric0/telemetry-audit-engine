import logging
from fastapi import APIRouter, status

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/nodes")
def get_active_nodes():
    return {"message": "You have reached the nodes endpoint", "status_code": status.HTTP_200_OK}

@router.post("/nodes/{node_id}/ingest")
def log_data(node_id: str):
    logger.info(f"You have reached node: {node_id}")
    return {"node_id": node_id, "status_code": status.HTTP_201_CREATED}