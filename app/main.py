from fastapi import FastAPI
from app.api.v1.endpoints import ingest
from app.core.deps import db_lifespan
from app.core.config import settings

app = FastAPI(title="Industrial Telemetry Audit Engine", lifespan=db_lifespan)

app.include_router(ingest.router, prefix=settings.API_V1_STR, tags=["ingest"])

@app.get("/")
async def read_root():
    return {"status": "operational", "version": "v1"}
