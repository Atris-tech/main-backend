from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import settings
from .mail_body_return_service import mail_body

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_TLS=settings.MAIL_TLS,
    MAIL_SSL=settings.MAIL_SSL
)


async def send_mail(email, mail_type, email_data):
    html = mail_body(type=mail_type, data=email_data)
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email,  # List of recipients, as many as you can pass
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
