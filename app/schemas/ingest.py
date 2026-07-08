from pydantic import BaseModel

class IngestResponse(BaseModel):
    status_code: int
    node_id: str
    processed_records: str
    message: str