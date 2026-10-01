from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


from database import SessionLocal
from models import ChatSession


with SessionLocal() as session:
    chat = ChatSession(
        chat_id="test-002",
        agent_name="Shalva",
        channel="live_chat",
        started_at=datetime(2026, 10, 1, 10, 0, 0),
        ended_at=datetime(2026, 10, 1, 10, 12, 30),
    )

    session.add(chat)
    try:
        session.commit()
        print("Saved! Row id:", chat.id, "| received at:", chat.received_at)
    except IntegrityError:
        session.rollback()
        print("Duplicate chat", chat.chat_id, "- already saved, skipping. ")

    all_chats = session.scalars(select(ChatSession)).all()
    for c in all_chats:
        duration = c.ended_at - c.started_at
        print(c.chat_id, c.agent_name, c.channel, "| handle time:", duration)
