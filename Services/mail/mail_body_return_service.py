def mail_body(type, data):
    if type == "verify":
        html = open("Services/mail/verify_email.html").read().format(user=data["user"], url=data["url"])
        return html
    elif type == "forgot":
        html = open("Services/mail/forgot-password.html").read().format(user=data["user"], url=data["url"])
        return html
