import asyncio
from dataclasses import dataclass
from typing import List

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from qdrant_client.http.models import Filter

from app.core.config import settings
from app.vector.qdrant import get_qdrant_client, ensure_collection
from app.vector.embeddings import EmbeddingService


@dataclass
class RetrievedDoc:
    text: str
    score: float


class RagPipeline:
    def __init__(self) -> None:
        self._llm = ChatOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            model=settings.llm_model,
            temperature=0.2,
        )
        self._embeddings = EmbeddingService()
        self._prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant. Use the context to answer."),
                ("human", "Question: {question}\n\nContext:\n{context}"),
            ]
        )

    async def retrieve(self, question: str, limit: int = 4) -> List[RetrievedDoc]:
        client = await get_qdrant_client()
        await ensure_collection(client, self._embeddings.vector_size)
        vector = await asyncio.to_thread(self._embeddings.embed_query, question)
        hits = await client.search(
            collection_name=settings.qdrant_collection,
            query_vector=vector,
            limit=limit,
            query_filter=Filter(must=[]),
        )
        return [RetrievedDoc(text=hit.payload.get("text", ""), score=hit.score) for hit in hits]

    async def generate(self, question: str, context: str) -> str:
        chain = self._prompt | self._llm
        result = await chain.ainvoke({"question": question, "context": context})
        return result.content

    async def run(self, question: str) -> str:
        docs = await self.retrieve(question)
        context = "\n\n".join([f"- {d.text}" for d in docs])
        return await self.generate(question, context)
