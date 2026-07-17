import datetime
import json
from typing import List, Any
from chromadb.api import ClientAPI, Metadata

SAMPLE_TELEMETRY: List[dict[str, Any]] = [
    {
        "node_id": "inv_alpha",
        "timestamp": datetime.datetime(2026, 7, 14, 8, 30, 0),
        "metric_type": "power_quality",
        "data_summary": "Inverter Alpha normal operation",
        "structured_metrics": {"voltage": 230, "current": 18, "harmonic_distortion": 1.2},
        "status_code": 0,
    },
    {
        "node_id": "inv_alpha",
        "timestamp": datetime.datetime(2026, 7, 14, 8, 35, 0),
        "metric_type": "power_quality",
        "data_summary": "Inverter Alpha voltage sag to 195V",
        "structured_metrics": {"voltage": 195, "current": 25, "harmonic_distortion": 3.8},
        "status_code": 1,
    },
    {
        "node_id": "pump_beta",
        "timestamp": datetime.datetime(2026, 7, 14, 9, 10, 0),
        "metric_type": "vibration",
        "data_summary": "Pump Beta bearing temperature elevated",
        "structured_metrics": {"temperature": 87, "vibration_rms": 4.5, "status_code": 2},
        "status_code": 2,
    },
    {
        "node_id": "inv_alpha",
        "timestamp": datetime.datetime(2026, 7, 14, 10, 0, 0),
        "metric_type": "error",
        "data_summary": "Inverter Alpha overcurrent trip",
        "structured_metrics": {"voltage": 0, "current": 0, "fault_code": "OC1"},
        "status_code": 3,
    },
    {
        "node_id": "gen_gamma",
        "timestamp": datetime.datetime(2026, 7, 14, 11, 0, 0),
        "metric_type": "fuel_consumption",
        "data_summary": "Generator Gamma fuel consumption spike during palm-fuel processing",
        "structured_metrics": {"fuel_rate": 120, "efficiency": 0.72, "load": 85},
        "status_code": 0,
    },
]

def seed_database(client: ClientAPI, collection_name: str = "industrial_telemetry_store"):
    collection = client.get_or_create_collection(collection_name)
    if collection.count() == 0:
        ids: List[str] = []
        documents: List[str] = []
        metadatas: List[Metadata] = []
        for entry in SAMPLE_TELEMETRY:
            doc_id = f"{entry['node_id']}_{entry['timestamp'].timestamp()}"
            ids.append(doc_id)
            documents.append(entry["data_summary"])
            metadatas.append({
                "node_id": entry["node_id"],
                "timestamp": entry["timestamp"].isoformat(),
                "timestamp_epoch": entry["timestamp"].timestamp(), 
                "metric_type": entry["metric_type"],
                "status_code": str(entry["status_code"]),
                "structured_metrics_json": json.dumps(entry["structured_metrics"]),
            })
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)