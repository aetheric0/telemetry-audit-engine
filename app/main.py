from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.v1.endpoints import ingest, prune_chroma, query, diagnose
from app.core.deps import db_lifespan
from app.core.config import settings

app = FastAPI(title="Industrial Telemetry Audit Engine", lifespan=db_lifespan)

app.include_router(ingest.router, prefix=settings.API_V1_STR, tags=["ingest"])
app.include_router(query.router, prefix=settings.API_V1_STR, tags=["query"])
app.include_router(diagnose.router, prefix=settings.API_V1_STR, tags=["diagnostics"])
app.include_router(prune_chroma.router, prefix=settings.API_V1_STR, tags=["prune"])

@app.get("/")
async def read_root():
    return {"status": "operational", "version": "v1"}

@app.get("/demo", response_class=HTMLResponse)
def demo():
    with open("app/static/demo.html") as f:
        return f.read()
