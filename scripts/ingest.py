import asyncio
from pathlib import Path

from app.vector.qdrant import get_qdrant_client, ensure_collection, upsert_documents
from app.vector.embeddings import EmbeddingService


def load_docs(data_dir: Path) -> list[dict]:
    docs: list[dict] = []
    for path in sorted(data_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            chunk = line.strip()
            if not chunk:
                continue
            docs.append({"text": chunk, "source": path.name})
    return docs


async def main() -> None:
    docs = load_docs(Path("data"))
    if not docs:
        raise RuntimeError("No .txt documents found in data directory")

    embeddings = EmbeddingService()
    vectors = await asyncio.to_thread(
        embeddings.embed_documents, [doc["text"] for doc in docs]
    )

    client = await get_qdrant_client()
    await ensure_collection(client, embeddings.vector_size)
    payloads = [{"text": doc["text"], "source": doc["source"]} for doc in docs]
    await upsert_documents(client, vectors, payloads)


if __name__ == "__main__":
    asyncio.run(main())
