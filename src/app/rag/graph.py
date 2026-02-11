from typing import TypedDict, List

from langgraph.graph import StateGraph, END

from app.rag.pipeline import RagPipeline, RetrievedDoc


class RagState(TypedDict):
    question: str
    docs: List[RetrievedDoc]
    answer: str


pipeline = RagPipeline()


async def retrieve_node(state: RagState) -> RagState:
    docs = await pipeline.retrieve(state["question"])
    return {"docs": docs}


async def generate_node(state: RagState) -> RagState:
    context = "\n\n".join([f"- {d.text}" for d in state["docs"]])
    answer = await pipeline.generate(state["question"], context)
    return {"answer": answer}


def build_graph():
    graph = StateGraph(RagState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
