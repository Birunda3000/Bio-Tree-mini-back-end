from os import path

from flask_mail import Message

from app.main import app, mail


def send_email(subject: str, html: str, to: list):
    msg = Message(
        subject=subject, sender=app.config["MAIL_USERNAME"], recipients=to, html=html
    )
    mail.send(msg)


def send_email_activation(to: str, professional_name: str, token: str) -> None:
    subject = "Account activation"
    link = "http://localhost:3000/user/activate/?token=" + token
    filename = path.join("app", "main", "templates", "activation_email_template.html")
    with open(filename, encoding="utf-8") as f:
        html = f.read().replace("%%$$%%", link)
        html = html.replace("%%@@%%", professional_name.lower().title())
    send_email(subject, html, [to])


def send_email_recovery(to: str, professional_name: str, token: str) -> None:
    subject = "Redefine password"
    link = "http://localhost:3000/user/password/forgot/?token=" + token
    filename = path.join("app", "main", "templates", "redefine_password_template.html")
    with open(filename, encoding="utf-8") as f:
        html = f.read().replace("%%$$%%", link)
        html = html.replace("%%@@%%", professional_name.lower().title())
    send_email(subject, html, [to])
