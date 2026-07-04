from pydantic import BaseModel
from datetime import datetime

class PayloadTelemetry(BaseModel):
    timestamp: datetime
    node_id: str
    voltage: float
    harmonic_distortion: float
    status_code: int