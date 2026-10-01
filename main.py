from fastapi import FastAPI, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import SessionLocal
from models import ChatSession
from schemas import ChatWebhookPayload


app = FastAPI(title="Support KPI Engine")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/webhook")
def receive_chat(payload: ChatWebhookPayload, db: Session = Depends(get_db)):
    chat = ChatSession(
        chat_id=payload.chat_id,
        agent_name=payload.agent_name,
        channel=payload.channel,
        started_at=payload.started_at,
        ended_at=payload.ended_at,

    )
    db.add(chat)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"status": "duplicate", "chat_id": payload.chat_id}

    return {"status": "saved", "chat_id": payload.chat_id, "id": chat.id}
