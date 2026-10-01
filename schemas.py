from datetime import datetime
from pydantic import BaseModel, Field


class ChatWebhookPayload(BaseModel):
    chat_id: str = Field(min_length=1, max_length=100)
    agent_name: str = Field(min_length=1, max_length=100)
    channel: str = Field(min_length=1, max_length=100)
    started_at: datetime
    ended_at: datetime | None = None
