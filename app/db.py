import chromadb

chroma_client = chromadb.PersistentClient(path='C:\\Users\\ADMIN\\dev\\node_tel\\src\\.persistent_storage')

# Test client connection
print(chroma_client.heartbeat())

collection = chroma_client.get_or_create_collection(name="my_collection")

# 1. Provide manual placeholder embeddings (e.g., 384-dimensional vectors)
# This completely bypasses the remote ONNX download block.
# mock_embedding_1 = [0.1] * 384
# mock_embedding_2 = [0.5] * 384

collection.upsert(
    ids=["id1", "id2"],
    # embeddings=[mock_embedding_1, mock_embedding_2],
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ]
)

# 2. When querying, you must pass a matching query vector instead of raw text
# mock_query_embedding = [0.12] * 384

results = collection.query(
    # query_embeddings=[mock_query_embedding],
    query_texts=["This is a document about florida"],
    n_results=2
)
print(results)