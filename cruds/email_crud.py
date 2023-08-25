import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session
from cruds import user_crud as crud_user
from cruds import security_crud as crud_security

load_dotenv()


def send_confirm_email(db: Session, user_email: str, token: str):
    email_sender = os.getenv('SENDER_EMAIL')
    email_password = os.getenv('SENDER_PASSWORD')
    email_receiver = user_email
    user = crud_user.get_user_by_email(db=db, email=email_receiver)

    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = 'Confirmação de email - Investing Brazil'

    html = f"""
    <html>
        <body>
            <p>Olá, {user.first_name} {user.last_name}</p>
            <p>Para confirmar seu email, clique no link abaixo:</p>
                <a href="https://v1.investingbrazil.online/email/confirm_email/{token}">Confirmar email</a>
        </body>
    </html>
    """

    message.attach(MIMEText(html, 'html'))

    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, message.as_string())
        server.quit()


def confirm_email(db: Session, user_email: str, token: str):
    user = crud_user.get_user_by_email(db=db, email=user_email)
    token_verify = crud_security.get_confirm_email_token(db=db, email=user_email)
    print(token_verify, user)
    if token_verify and user:
        user.email_activated = True
        db.commit()
        db.refresh(user)
        crud_security.delete_verified_token(db=db, token=token_verify.id)
        return True
    raise HTTPException(status_code=404, detail="Token inválido ou expirado!")


def send_password_reset_mail(db: Session, user_email: str):

    email_sender = os.getenv('SENDER_EMAIL')
    email_password = os.getenv('SENDER_PASSWORD')
    email_receiver = user_email

    user = crud_user.get_user_by_email(db=db, email=user_email)
    token = crud_security.generate_reset_password_token()
    crud_security.save_reset_password_token(db=db, user_id=user.id, token=token)

    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = 'Redefinição de senha - Investing Brazil'

    html = f"""
    <html>
        <body>
            <p>Olá, {user.first_name} {user.last_name}</p>
            <p>Para redefinir sua senha, clique no link abaixo:</p>
            <a href="https://v1.investingbrazil.online/email/confirm_password_reset/{token}">Redefinir senha</a>
        </body>
    </html>
    """

    message.attach(MIMEText(html, 'html'))

    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, message.as_string())
        server.quit()
