# RAG Agent Platform

Production-style backend platform for building domain agents with retrieval-augmented generation.

- FastAPI services
- LangChain + LangGraph RAG pipelines
- Vector DB (Qdrant)
- Relational DB (PostgreSQL)
- Asyncio + async DB access
- Dockerized local environment
- OpenAI-compatible LLM API integration (DeepSeek supported)

## Architecture

- `src/app/main.py` - FastAPI app entry point
- `src/app/api/router.py` - HTTP endpoints
- `src/app/agents/` - agent implementations
- `src/app/rag/` - RAG pipeline + LangGraph orchestration
- `src/app/db/` - async SQLAlchemy session + repository
- `src/app/vector/` - Qdrant integration
- `scripts/ingest.py` - ingestion pipeline for vector search

## Quick start (Docker)

1) Create `.env` from `.env.example` and set your API key.
2) Run services:

```bash
docker compose up --build
```

3) Ingest knowledge base:

```bash
docker compose exec api python scripts/ingest.py
```

4) Query RAG:

```bash
curl -X POST http://localhost:8000/rag/query -H "Content-Type: application/json" -d '{"question":"What is LangGraph?"}'
```

5) Run agent:

```bash
curl -X POST http://localhost:8000/agents/run -H "Content-Type: application/json" -d '{"agent_name":"support","input_text":"Explain RAG"}'
```

## Local dev (without Docker)

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
set PYTHONPATH=src
uvicorn app.main:app --reload
```

## Notes

- Embeddings are local by default (`EMBEDDING_PROVIDER=local_hash`) for predictable local runs.
- You can switch embeddings provider to OpenAI-compatible endpoints through `.env`.
