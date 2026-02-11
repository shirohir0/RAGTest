import hashlib
from typing import Sequence

from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


class EmbeddingService:
    def __init__(self) -> None:
        self._provider = settings.embedding_provider.strip().lower()
        self._vector_size = max(8, settings.embedding_vector_size)
        self._remote = None
        if self._provider == "openai":
            api_key = settings.embedding_api_key or settings.llm_api_key
            base_url = settings.embedding_base_url or settings.llm_base_url
            self._remote = OpenAIEmbeddings(
                api_key=api_key,
                base_url=base_url,
                model=settings.embeddings_model,
            )

    @property
    def vector_size(self) -> int:
        if self._provider == "openai":
            # Keep the configured size for collection checks.
            return self._vector_size
        return self._vector_size

    def embed_query(self, text: str) -> list[float]:
        if self._remote is not None:
            return self._remote.embed_query(text)
        return self._local_embed(text)

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        if self._remote is not None:
            return self._remote.embed_documents(list(texts))
        return [self._local_embed(text) for text in texts]

    def _local_embed(self, text: str) -> list[float]:
        # Stable, dependency-free embedding fallback for local/dev use.
        vector = [0.0] * self._vector_size
        tokens = text.lower().split()
        if not tokens:
            return vector
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = int.from_bytes(digest[:4], "big") % self._vector_size
            sign = 1.0 if (digest[4] % 2 == 0) else -1.0
            vector[idx] += sign
        norm = sum(v * v for v in vector) ** 0.5
        if norm == 0:
            return vector
        return [v / norm for v in vector]
