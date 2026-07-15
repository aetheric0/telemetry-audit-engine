from chromadb import Collection
from app.schemas.query import TelemetrySearchRequest, TelemetrySearchMatch, TelemetrySearchResponse

class TelemetryRepository:
    def __init__(self, collection: Collection):
        self.collection = collection
    
    def semantic_search(self, search_params: TelemetrySearchRequest):
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
        formatted_matches = []

        # Verify if any results were returned to avoid IndexError
        if raw_results and raw_results["ids"] and len(raw_results["ids"][0]) > 0:
            documents = raw_results["documents"][0]
            distances = raw_results["distances"][0]
            metadatas = raw_results["metadatas"][0]

            for i in range(len(ids)):
                match_item = TelemetrySearchMatch(
                    id=ids[1],
                    document=documents[i]
                    distance=round(distances[i], 4)     #clean floating-point precision
                    metadata=metadatas[i] if metadatas[i] else {}
                )
                formatted_matches.append(match_item)
    
    return TelemetrySearchResponse(
        query = search_params.query_text,
        matches=formatted_matches
    )