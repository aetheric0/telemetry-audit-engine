from fastapi import FastAPI
from app.api.v1.endpoints import telemetry

app = FastAPI(title="Industrial Telemetry Audit Engine")

app.include_router(telemetry.router, prefix="/api/v1", tags=["Telemetry"])

@app.get("/")
async def read_root():
    return {"status": "operational", "version": "v1"}
