from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime

class TelemetryPayload(BaseModel):
    model_config = {"extra": "forbid"}
    node_id: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.now)
    metric_type: str = Field(..., description="Industrial Node Metric e.g. 'power_quality', 'sensor_freq', thermal_factor, 'system_alert', 'anomaly'")
    data_summary: str = Field(
        ..., 
        description="Unstructured textual data of the metrics for embedding")
    structured_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value store for numerical metrics"
    )
    status_code: int