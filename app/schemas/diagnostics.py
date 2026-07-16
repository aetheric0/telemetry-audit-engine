from typing import List
from pydantic import BaseModel

class DiagnosticResponse(BaseModel):

        query: str
        diagnosis: str
        sources: List[str]
