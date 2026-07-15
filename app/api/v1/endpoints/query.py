from fastapi import APIRouter, Depends, HTTPException
from chromadb.api import ClientAPI
from app.schemas.query import TelemetrySearchRequest, TelemetrySearchResponse
from app.repositories.telemetry import TelemetryRepository
from app.core.deps import get_chroma_db

router = APIRouter()

@router.get('/query', response_model=TelemetrySearchResponse)
def query_db(search_params: TelemetrySearchRequest,db: ClientAPI = Depends(get_chroma_db)) -> TelemetrySearchResponse:
    """
    Exposes a natural language semantic search endpoint over historical asset telemetry.
    Runs entirely within FastAPI's thread pool to isolate local disk blocking.
    """
    collection = db.get_collection(name="industrial_telemetry_store")
    try:
        telemetry_repo = TelemetryRepository(collection=collection)
        response = telemetry_repo.semantic_search(search_params)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute vector matrix lookup: {str(e)}"
        )