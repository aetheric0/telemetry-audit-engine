import concurrent.futures
from typing import Any
import requests
import time

i: int = 0

url = "http://localhost:8000/api/v1/nodes/test_node/ingest"
payload: dict[str, Any] = {
    "node_id": "test_node",
    "timestamp": "2026-07-16T12:00:00Z",
    "metric_type": "test",
    "data_summary": "concurrent stress test " * 10,  # slightly longer text
    "structured_metrics": {"value": i},
    "status_code": 0
}

def send(i: int):
    p = payload.copy()
    p["structured_metrics"] = {"value": i}
    start = time.time()
    r = requests.post(url, json=p, timeout=10)
    return r.status_code, r.json().get("message"), time.time() - start

with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(send, i) for i in range(100)]  # 100 requests
    for f in concurrent.futures.as_completed(futures):
        code, msg, elapsed = f.result()
        print(f"Status {code}, time {elapsed:.2f}s, message: {msg}")