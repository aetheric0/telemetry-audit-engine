from pydantic import BaseModel, ConfigDict, Field
from typing import Any
from datetime import datetime

class TelemetryPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    node_id: str = Field(
        ...,
        description="Unique identifire for the edge node asset"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="UTC isolation timestamp"
    )
    metric_type: str = Field(
        ...,
        description="Node Metric e.g. 'power_quality', 'time-series data'"
    )
    data_summary: str = Field(
        ..., 
        description="Unstructured textual data of the metrics for" \
        "embedding calculations"
    )
    structured_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value store for numerical metrics"
    )
    status_code: int = Field(
        ..., 
        description="Operational status code from the hardware node loop"
    )