from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "RAG Agent Platform"
    app_version: str = "0.1.0"

    database_url: str = "postgresql+asyncpg://app:app@localhost:5432/app"

    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "docs"

    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com"
    llm_model: str = "deepseek-chat"

    embedding_provider: str = "local_hash"
    embeddings_model: str = "text-embedding-3-small"
    embedding_base_url: str = ""
    embedding_api_key: str = ""
    embedding_vector_size: int = 384


settings = Settings()
