from datetime import datetime, timezone
from pydantic import BaseModel, Field, AwareDatetime, field_validator, model_validator


class ChatWebhookPayload(BaseModel):
    chat_id: str = Field(min_length=1, max_length=100)
    agent_name: str = Field(min_length=1, max_length=100)
    channel: str = Field(min_length=1, max_length=50)
    started_at: AwareDatetime
    ended_at: AwareDatetime | None = None

    @field_validator("started_at", "ended_at", mode="before")
    @classmethod
    def reject_unix_timestamps(cls, value):
        if isinstance(value, (int, float)):
            raise ValueError(
                "must be an ISO 8601 datetime string, not a number")
        if isinstance(value, str) and value.strip().replace(".", "", 1).isdigit():
            raise ValueError(
                "must be an ISO 8601 datetime string, not a number")
        return value

    @field_validator("started_at", "ended_at")
    @classmethod
    def convert_to_utc(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def check_end_after_start(self):
        if self.ended_at is not None and self.ended_at < self.started_at:
            raise ValueError("ended_at must not be before started_at")
        return self
