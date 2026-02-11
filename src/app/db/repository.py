from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.db.models import AgentRun


async def save_agent_run(session: AsyncSession, agent_name: str, input_text: str, output_text: str) -> None:
    stmt = insert(AgentRun).values(agent_name=agent_name, input_text=input_text, output_text=output_text)
    await session.execute(stmt)
    await session.commit()
