import logging
import chromadb
from chromadb.api import ClientAPI
from fastapi import FastAPI, Request
from .config import settings
from .seed import seed_database
from contextlib import asynccontextmanager


logging.basicConfig(filename=settings.LOG_FILE, encoding='utf-8', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    """Handles thread-safe initialization and teardown of ChromaDB."""
    persist_path = settings.CHROMA_PERSIST_DIR
    chroma_client = chromadb.PersistentClient(path=persist_path)
    
    # Pre-boot the collection here once so routes never run redundant lookup checks.
    chroma_client.get_or_create_collection(name="industrial_telemetry_store")

    seed_database(chroma_client)

    # Store the client reference inside the application state
    app.state.chroma_client = chroma_client

    yield

    logger.info("Securely flushing memory buffers and closing database.")

def get_chroma_db(request: Request) -> ClientAPI:
    """Injects the running client instance into endpoint operations."""
    return request.app.state.chroma_client
    

