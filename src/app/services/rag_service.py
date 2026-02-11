from app.rag.pipeline import RagPipeline


class RagService:
    def __init__(self) -> None:
        self._pipeline = RagPipeline()

    async def ask(self, question: str) -> str:
        return await self._pipeline.run(question)
