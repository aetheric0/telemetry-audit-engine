from fastapi import APIRouter, Depends
from chromadb.api import ClientAPI
from app.core.deps import get_chroma_db

router = APIRouter()

@router.get('/query')
def query_db(db: ClientAPI = Depends(get_chroma_db)):
    pass