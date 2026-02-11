from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.db.repository import save_agent_run
from app.schemas.rag import QueryRequest, QueryResponse, AgentRunRequest, AgentRunResponse
from app.services.rag_service import RagService
from app.services.agent_service import AgentService

api_router = APIRouter()
rag_service = RagService()
agent_service = AgentService()


@api_router.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@api_router.post("/rag/query", response_model=QueryResponse)
async def rag_query(payload: QueryRequest) -> QueryResponse:
    answer = await rag_service.ask(payload.question)
    return QueryResponse(answer=answer)


@api_router.post("/agents/run", response_model=AgentRunResponse)
async def agents_run(payload: AgentRunRequest, session: AsyncSession = Depends(get_session)) -> AgentRunResponse:
    try:
        output = await agent_service.run(payload.agent_name, payload.input_text)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    await save_agent_run(session, payload.agent_name, payload.input_text, output)
    return AgentRunResponse(output_text=output)
