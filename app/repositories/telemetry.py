import threading
from typing import List

from chromadb import Collection, Metadata
from app.schemas.query import TelemetrySearchRequest, TelemetrySearchMatch, TelemetrySearchResponse

# Module-level lock for all ChromaDB write operations

_write_lock = threading.Lock()

class TelemetryRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def store_with_lock(self, ids: List[str], documents: List[str], metadatas: List[Metadata] | None):
        """ Thread-safe upsert with lock.
        """
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
    
    def semantic_search(self, search_params: TelemetrySearchRequest) -> TelemetrySearchResponse:
        """
        Executes a localized semantic distance lookup across the vector store.
        Uses standard def because local file-backed HNSW lookups are blocking.
        """
        # ChromaDB automatically vectorizes the raw query text using its internal embedding model
        raw_results = self.collection.query(
            query_texts=[search_params.query_text],
            n_results=search_params.n_results
        )

        # Unpack ChromaDB's highly nested array matrix structure safely
        formatted_matches: List[TelemetrySearchMatch] = []

        ids_batch = raw_results.get("ids")
        documents_batch = raw_results.get("documents")
        distances_batch = raw_results.get("distances")
        metadatas_batch = raw_results.get("metadatas")

        # Verify if any results were returned to avoid IndexError
        if (
            ids_batch 
            and documents_batch is not None
            and distances_batch is not None
            and metadatas_batch is not None
        ):
            ids = ids_batch[0]
            documents = documents_batch[0]
            distances = distances_batch[0]
            metadatas = metadatas_batch[0]

            for i in range(len(ids)):
                doc_text = str(documents[i])
                dist_val = float(distances[i])
                meta_dict = dict(metadatas[i])

                match_item = TelemetrySearchMatch(
                    id=ids[i],
                    document=doc_text,
                    distance=round(dist_val, 4),     #clean floating-point precision
                    metadata= meta_dict
                )
                formatted_matches.append(match_item)
    
        return TelemetrySearchResponse(
            query = search_params.query_text,
            matches=formatted_matches
        )