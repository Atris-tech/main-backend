import os
from settings import PROJECT_DIR


def mail_body(type, data):
    if type == "verify":
        html = open(os.path.join(PROJECT_DIR, "Services/mail/verify_email.html")).read().format(user=data["user"],
                                                                                                url=data["url"])
        return html
    elif type == "forgot":
        html = open(os.path.join(PROJECT_DIR,"Services/mail/forgot-password.html")).read().format(user=data["user"],
                                                                                                  url=data["url"])
        return html
