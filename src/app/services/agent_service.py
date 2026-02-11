from app.agents.support_agent import SupportAgent


class AgentService:
    def __init__(self) -> None:
        self._agents = {
            "support": SupportAgent(),
        }

    async def run(self, agent_name: str, text: str) -> str:
        agent = self._agents.get(agent_name)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_name}")
        return await agent.run(text)
