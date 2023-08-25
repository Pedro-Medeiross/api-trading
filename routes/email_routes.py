from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connection import SessionLocal
from cruds import security_crud as crud_security
from cruds import user_crud as crud_user
from cruds import email_crud as crud_email
from fastapi.responses import RedirectResponse

email_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@email_router.get('/confirm_email/{token}')
def confirm_email(token: str, db: Session = Depends(get_db)):
    crud_security.verify_confirm_email_token(db=db, token=token)
    return RedirectResponse('https://investingbrazil.online/')


@email_router.get('/send_password_reset/{email}')
def send_password_reset(email: str, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Email incorreto ou não encontrado!")
    crud_email.send_password_reset_mail(db=db, user_email=user.email)
    return {'message': 'Email enviado com sucesso!'}


@email_router.get('/confirm_password_reset/{token}')
def password_reset(token: str, db: Session = Depends(get_db)):
    validated = crud_security.verify_password_reset_token(db=db, token=token)
    return validated
