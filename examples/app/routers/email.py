from typing import List

from fastapi import APIRouter, Request
from popol.email.globals import email
from popol.email.message import Message
from pydantic import BaseModel, EmailStr

from app.settings import settings


class SendEmail(BaseModel):
    recipients: List[EmailStr]
    text: str
    subject: str


router = APIRouter(prefix="/email", tags=["email"])


@router.post("/send", summary="Send an email")
async def send_email(request: Request, body: SendEmail):
    message = Message(
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipients=body.recipients,
        subject=body.subject,
        text=body.text,
    )
    await email.send(message)
    return {"detail": "Email sent"}
