from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Any

class TelemetrySearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query_text: str = Field(
        ...,
        description="Natural language description of the hardware state or anomaly to find",
        #example="voltage spikes above normal thresholds during palm-fuel processing",
    )
    n_results: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number highly similar log instances to return",
    )

class TelemetrySearchMatch(BaseModel):
    id: str
    document: str
    distance: float
    metadata: Dict[str, Any]

class TelemetrySearchResponse(BaseModel):
    query: str
    matches: List[TelemetrySearchMatch]