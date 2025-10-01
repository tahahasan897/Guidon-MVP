from pydantic import BaseModel
import os


class Settings(BaseModel):
    env: str = os.getenv("ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://founder:founder_pw@db:5432/founder")

    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    rq_worker_concurrency: int = int(os.getenv("RQ_WORKER_CONCURRENCY", "2"))

    nextauth_secret: str = os.getenv("NEXTAUTH_SECRET", "")
    nextauth_url: str = os.getenv("NEXTAUTH_URL", "")

    litellm_model: str = os.getenv("LITELLM_MODEL", "gpt-4o-mini")
    litellm_api_base: str = os.getenv("LITELLM_API_BASE", "https://api.openai.com/v1")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    google_redirect_uri: str = os.getenv("GOOGLE_REDIRECT_URI", "")

    notion_client_id: str = os.getenv("NOTION_CLIENT_ID", "")
    notion_client_secret: str = os.getenv("NOTION_CLIENT_SECRET", "")
    notion_redirect_uri: str = os.getenv("NOTION_REDIRECT_URI", "")

    slack_bot_token: str = os.getenv("SLACK_BOT_TOKEN", "")
    slack_signing_secret: str = os.getenv("SLACK_SIGNING_SECRET", "")

    encryption_key: str = os.getenv("ENCRYPTION_KEY", "")

    agent_max_tool_calls: int = int(os.getenv("AGENT_MAX_TOOL_CALLS", "10"))
    agent_max_seconds: int = int(os.getenv("AGENT_MAX_SECONDS", "60"))
    agent_max_cost_usd: float = float(os.getenv("AGENT_MAX_COST_USD", "1.0"))


settings = Settings()  # type: ignore[call-arg]
