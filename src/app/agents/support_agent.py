from app.agents.base import BaseAgent
from app.rag.graph import build_graph


class SupportAgent(BaseAgent):
    name = "support"

    def __init__(self) -> None:
        self._graph = build_graph()

    async def run(self, text: str) -> str:
        state = await self._graph.ainvoke({"question": text})
        return state["answer"]
