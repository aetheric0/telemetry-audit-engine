from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from chromadb.api import ClientAPI

from app.core.deps import get_chroma_db
from app.schemas.query import TelemetrySearchRequest, TelemetrySearchResponse, TelemetrySearchMatch
#from app.schemas.diagnostics import DiagnosticResponse
from app.repositories.telemetry import TelemetryRepository
from app.services.custom_prompt import build_diagnostic_prompt
from app.services.llm_service import LLMService
#from app.services.rag_service import RAGService


router = APIRouter()

@router.post("/diagnose")
def diagnose(search_params: TelemetrySearchRequest, db: ClientAPI = Depends(get_chroma_db)) -> StreamingResponse:
    telemetry_repo = TelemetryRepository(collection = db.get_collection("industrial_telemetry_store"))
    search_response: TelemetrySearchResponse = telemetry_repo.semantic_search(search_params)
    query_matches: List[TelemetrySearchMatch] = search_response.matches

    # Build prompt
    prompt = build_diagnostic_prompt(search_params.query_text, query_matches)

    # Create LLM Service
    llm = LLMService()

    async def token_generator():
        async for token in llm.generate_stream(prompt, demo_mode=True):
            yield token

    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )
    


    
    
    # answer = llm.generate_response(prompt)

    # return DiagnosticResponse(
    #     query=search_params.query_text,
    #     diagnosis=answer,
    #     sources=[m.id for m in query_matches]
    # )