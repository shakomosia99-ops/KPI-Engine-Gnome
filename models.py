from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, engine


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    agent_name: Mapped[str] = mapped_column(String(100))
    channel: Mapped[str] = mapped_column(String(50))
    started_at: Mapped[datetime] = mapped_column()
    ended_at: Mapped[datetime | None] = mapped_column()
    received_at: Mapped[datetime] = mapped_column(server_default=func.now())


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables created! ")
