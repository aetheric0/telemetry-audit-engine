from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import APIRouter, Depends
from app.core.deps import get_chroma_db
from chromadb.api import ClientAPI

router = APIRouter(prefix="/admin")

@router.post("/prune")
def prune_old_logs(db: ClientAPI = Depends(get_chroma_db), days_to_keep: int = 30) -> dict[str, Any]:
    collection = db.get_collection(name="industrial_telemetry_store")
    cut_off_epoch = (datetime.now(timezone.utc) - timedelta(days=days_to_keep)).timestamp()
    before = collection.count()
    collection.delete(
        where= {
        "$and": [
            {"timestamp": {"$lt": cut_off_epoch}}, 
             {"status_code": 0}
            ]
        }
    )
    after = collection.count()
    return {
        "message": f"Pruned records older than {days_to_keep} days",
        "deleted_count": before - after,
        "remaining_records": after
    }

@router.post("/reset")
def reset_collection(db: ClientAPI = Depends(get_chroma_db)):
    try:
        db.delete_collection("industrial_telemetry_store")
    except Exception as e:
        raise Exception(f"Could not delete collection: {e}")
    # The lifespan or a subsequent call can re-create and seed
    return {"message": "Collection deleted. Restart the app to re‑seed."}