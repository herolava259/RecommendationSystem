from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType, NameEmail
from config import Config
from pathlib import Path
from typing import List, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

mail_config = ConnectionConfig(
    MAIL_USERNAME= Config.MAIL_USERNAME,
    MAIL_PASSWORD= Config.MAIL_PASSWORD,
    MAIL_PORT=587,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    # TEMPLATE_FOLDER= TEMPLATES_DIR
)

mail = FastMail(config=mail_config)

def create_message(recipients: List[Tuple[str, str]], subject: str, body: str):
    recipients: List[NameEmail] = [NameEmail(*e) for e in recipients]
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html,
    )

    return message