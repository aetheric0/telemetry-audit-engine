from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from chromadb.api import ClientAPI

from app.core.deps import get_chroma_db
from app.schemas.query import TelemetrySearchRequest, TelemetrySearchResponse, TelemetrySearchMatch
from app.repositories.telemetry import TelemetryRepository
from app.services.custom_prompt import build_diagnostic_prompt
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/diagnose")
def diagnose(search_params: TelemetrySearchRequest, db: ClientAPI = Depends(get_chroma_db)) -> StreamingResponse:
    telemetry_repo = TelemetryRepository(collection=db.get_collection("industrial_telemetry_store"))
    search_response: TelemetrySearchResponse = telemetry_repo.semantic_search(search_params)
    query_matches: List[TelemetrySearchMatch] = search_response.matches

    prompt = build_diagnostic_prompt(search_params.query_text, query_matches)
    llm = LLMService()

    async def token_generator():
        async for token in llm.generate_stream(prompt, demo_mode=False):
            yield token

    async def sse_generator():
        async for token in token_generator():
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",   # <-- fixed
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache"
        }
    )