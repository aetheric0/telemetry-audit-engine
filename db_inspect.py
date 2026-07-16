import chromadb

client = chromadb.PersistentClient(path="./.chroma_storage")
collection = client.get_collection("industrial_telemetry_store")

results = collection.peek(limit=5)

print(results)

