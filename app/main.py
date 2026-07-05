import logging
from fastapi import FastAPI
from app.api.v1.endpoints import telemetry, ingest

logging.basicConfig(filename="logs.py", encoding='utf-8', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

app = FastAPI(title="Industrial Telemetry Audit Engine")

app.include_router(telemetry.router, prefix="/api/v1", tags=["Telemetry"])
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])

@app.get("/")
async def read_root():
    return {"status": "operational", "version": "v1"}
