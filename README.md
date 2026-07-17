# Industrial Telemetry AI Auditor

**Reduce incident diagnosis from hours to seconds with on‑prem, cost‑efficient AI.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-API-green)]([your-live-url])
[![Watch the video](https://img.shields.io/badge/Watch-Demo%20Video-blue)]([your-video-url])

## The Problem

Industrial and infrastructure teams drown in telemetry logs. When a node fails, engineers manually grep through gigabytes of unstructured data to find root causes. This takes hours, delays repairs, and costs money.

## The Solution

An intelligent, streaming API that:
- **Ingests** structured telemetry from edge nodes in real time.
- **Retrieves** historically similar failures using semantic search.
- **Diagnoses** root causes via a Llama 3.1 language model, streaming the answer token‑by‑token.

All on a **$5/month VPS** with **zero cloud vendor lock‑in** – your data stays local.

## Architecture at a Glance
**Edge Nodes → FastAPI → ChromaDB (vector store) → Llama 3.1 (Groq) → Streaming Diagnosis**
- **FastAPI** async endpoints with Pydantic v2 validation.
- **ChromaDB** embedded mode for zero‑infra vector search (cosine similarity).
- **Llama 3.1** via Groq for sub‑second, streaming diagnostic synthesis.
- **Background tasks** + **thread‑safe write lock** proven under 100‑request concurrent load tests.

## Key Engineering Decisions

| Decision | Rationale |
|----------|-----------|
| **Embedded ChromaDB over client‑server** | Zero operational overhead, keeps the entire system in one process for easy deployment. |
| **Thread‑lock on writes** | Empirically tested: without it, concurrent writes exhaust the thread pool under load (see `tests/stress_test.py`). The lock ensures graceful degradation, not timeout failures. |
| **Streaming response** | Users see diagnosis in real time |
| **No heavy framework** | Deliberately avoided LangChain/LlamaIndex to keep the pipeline transparent and debuggable. |
| **JSON‑serialized metrics in metadata** | Preserves rich structured data for LLM context without breaking ChromaDB’s flat metadata constraint. |

## Quick Start

### Prerequisites
- Python 3.11+
- Groq API key (free tier available)

### Local Run
```bash
git clone https://github.com/aetheric0/telemetry-audit-engine.git
cd telemetry-audit-engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your GROQ_API_KEY
uvicorn app.main:app --reload
```

### Docker
`docker compose up --build`

**API docs at http://localhost:8000/docs**

### Live Endpoints
- POST /api/v1/nodes/{node_id}/ingest – Submit telemetry
- POST /api/v1/diagnose – Natural language diagnostic query (streaming)

### Demo Video
Watch the 2‑minute walkthrough

### Why This Matters to Your Business
- Faster incident resolution – seconds, not hours.
- Predictable costs – no per‑query cloud fees.
- Data sovereignty – runs on your hardware.
- Auditable – every diagnosis is traceable to exact log sources.

## Data Lifecycle

- **Hot retention (ChromaDB):** all error records + rolling 30‑day window of routine telemetry. Pruning endpoint included (`/api/v1/endpoints/prune_chroma.py`).
- **Pruning:** Admin endpoint `POST /admin/prune?days_to_keep=30` deletes logs older than N days, keeping the vector store lean.
    - **TODO: Protect with admin API key or internal-only network access in production.**
- **Future work:** Integrate with a time‑series database (InfluxDB) for long‑term metrics storage, with automatic archive to object storage for compliance.

## Roadmap / Production Vision

- **Live streaming ingestion** via MQTT/WebSocket, with batching and back‑pressure control.
- **Time‑series storage** for raw metrics (InfluxDB/TimescaleDB) to complement the semantic log store.
- **Anomaly detection pipeline** that automatically creates diagnostic logs in ChromaDB when thresholds are breached.
- **Hybrid search** (keyword + vector) for even better retrieval accuracy.



### License