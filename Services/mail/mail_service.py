import json

import requests
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
#
# import settings
# from Services.mail.mail_body_return_service import mail_body
from settings import MAIL_GUN_API_KEY, MAIL_GUN_API_ENDPOINT

url = MAIL_GUN_API_ENDPOINT

# conf = ConnectionConfig(
#     MAIL_USERNAME=settings.MAIL_USERNAME,
#     MAIL_PASSWORD=settings.MAIL_PASSWORD,
#     MAIL_FROM=settings.MAIL_FROM,
#     MAIL_PORT=settings.MAIL_PORT,
#     MAIL_SERVER=settings.MAIL_SERVER,
#     MAIL_TLS=settings.MAIL_TLS,
#     MAIL_SSL=settings.MAIL_SSL
# )
#
#
# async def send_mail(email, mail_type, email_data, subject):
#     html = mail_body(type=mail_type, data=email_data)
#     message = MessageSchema(
#         subject=subject,
#         recipients=email,  # List of recipients, as many as you can pass
#         body=html,
#         subtype="html"
#     )
#
#     fm = FastMail(conf)
#     await fm.send_message(message)


def email_builder(to_email, variable_dict, subject, template):
    print(variable_dict)
    payload = {
        'from': 'atris@atrisapp.com',
        'to': to_email,
        'subject': subject,
        'template': template,
        'h:X-Mailgun-Variables': json.dumps(variable_dict)
    }
    headers = {
        'Authorization': 'Basic ' + MAIL_GUN_API_KEY
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
