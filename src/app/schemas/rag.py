from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


class AgentRunRequest(BaseModel):
    agent_name: str
    input_text: str


class AgentRunResponse(BaseModel):
    output_text: str
