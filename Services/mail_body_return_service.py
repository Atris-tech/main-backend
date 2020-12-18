def mail_body(type, data):
    if type == "verify":
        html = open("verify_email.html").read().format(user=data["user"], url=data["url"])
        return html
    elif type == "forgot":
        html = open("forgot-password.html").read().format(user=data["user"], url=data["url"])
        return html
