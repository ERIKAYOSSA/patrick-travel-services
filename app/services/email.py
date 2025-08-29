from email.message import EmailMessage
import aiosmtplib

# 📧 Confirmation de création de compte
async def send_confirmation_email(to_email: str, username: str):
    message = EmailMessage()
    message["From"] = "noreply@patricktravel.com"
    message["To"] = to_email
    message["Subject"] = "Bienvenue chez Patrick Travel Services"
    message.set_content(f"""
Bonjour {username},

Votre compte a bien été créé sur Patrick Travel Services 🎉

Vous pouvez maintenant accéder à nos services de visa, admission, logement et plus encore.

L’équipe Patrick Travel
""")

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="ton.email@gmail.com",         # 🔒 remplace par ton email
        password="ton_mot_de_passe_app"         # 🔒 mot de passe d'application
    )

# 🔔 Notification générique (message, mise à jour, relance…)
async def send_notification_email(to_email: str, subject: str, content: str):
    message = EmailMessage()
    message["From"] = "noreply@patricktravel.com"
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="ton.email@gmail.com",         # 🔒 même identifiants
        password="ton_mot_de_passe_app"
    )