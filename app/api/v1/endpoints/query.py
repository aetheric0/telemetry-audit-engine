from fastapi import APIRouter

router = APIRouter()

@router.get('/query')
def query_db():
    pass