from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from app.core.config import settings


async def get_qdrant_client() -> AsyncQdrantClient:
    return AsyncQdrantClient(url=settings.qdrant_url)


def _extract_vector_size(vectors_config: object) -> int | None:
    if hasattr(vectors_config, "size"):
        return int(vectors_config.size)
    if isinstance(vectors_config, dict):
        first = next(iter(vectors_config.values()), None)
        if first is not None and hasattr(first, "size"):
            return int(first.size)
    return None


async def ensure_collection(client: AsyncQdrantClient, vector_size: int) -> None:
    collections = await client.get_collections()
    if settings.qdrant_collection not in {c.name for c in collections.collections}:
        await client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        return
    info = await client.get_collection(collection_name=settings.qdrant_collection)
    existing_size = _extract_vector_size(info.config.params.vectors)
    if existing_size != vector_size:
        await client.recreate_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


async def upsert_documents(client: AsyncQdrantClient, vectors: list[list[float]], payloads: list[dict]) -> None:
    points = [PointStruct(id=idx, vector=vector, payload=payloads[idx]) for idx, vector in enumerate(vectors)]
    await client.upsert(collection_name=settings.qdrant_collection, points=points)
