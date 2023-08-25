import os
import secrets
import pytz
from typing import Optional
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, HTTPBasicCredentials, HTTPBasic
from dotenv import load_dotenv
from jose import JWTError, jwt
from connection import SessionLocal
from cruds import user_crud as crud_user
from cruds import email_crud as crud_email
from schemas import token_data as schemas_token
from models import tokens as models_token
import re


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 6

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    email_regex = r'^[\w\.\+\-]+\@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$|^[\w]+$'

    tz = pytz.timezone('America/Sao_Paulo')
    now = datetime.now(tz).replace(microsecond=0)

    if re.match(email_regex, username):
        if '@' in username:
            user = crud_user.get_user_by_email(db=db, email=username)
            if user:
                return user
        else:
            user = crud_user.get_user_by_username(db, username)
            if user:
                return user

    if not user:
        print('Usuário não encontrado ou incorreto')
        raise HTTPException(status_code=404, detail="Usuário incorreto ou não encontrado!")
    if not verify_password(password, user.password):
        print('Senha incorreta')
        raise HTTPException(status_code=404, detail="Senha incorreta")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=6)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Não autenticado/Logado!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas_token.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud_user.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_basic_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.getenv('API_USER'))
    correct_password = secrets.compare_digest(credentials.password, os.getenv('API_PASS'))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# def generate_confirm_email_token(email: str):
#     token = create_access_token(
#         data={"sub": email}, expires_delta=timedelta(hours=24)
#     )
#     return token
#
#
# def verify_confirm_email_token(db: Session, token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Token inválido")
#         user = crud_user.get_user_by_email(db=db, email=email)
#         token_data = get_confirm_email_token(db=db, email=user.email)
#         if user is None:
#             raise HTTPException(status_code=404, detail="Usuário não encontrado")
#         if token == token_data.token:
#             crud_email.confirm_email(db=db, user_email=user.email, token=token)
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token inválido")
#
#
# def get_confirm_email_token(db: Session, email: str):
#     user = crud_user.get_user_by_email(db, email)
#     if user is None:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")
#     if user.is_active:
#         raise HTTPException(status_code=401, detail="Usuário já ativado")
#     token = db.query(models_token.Tokens).filter(models_token.Tokens.user_id == user.id).first()
#     return token
#
#
# def delete_verified_token(db: Session, token: int):
#     get_token = db.query(models_token.Tokens).filter(models_token.Tokens.id == token).first()
#     if get_token is None:
#         raise HTTPException(status_code=404, detail="Token não encontrado")
#     db.delete(get_token)
#     db.commit()
#     return get_token
#
#
# def generate_reset_password_token():
#     token = secrets.token_hex(3)
#     return token
#
#
# def save_reset_password_token(db: Session, user_id: int, token: str):
#     user = crud_user.get_user_by_id(db=db, user_id=user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")
#     models_token.Tokens(user_id=user.id, token=token)
#
#
# def verify_password_reset_token(db: Session, token: str):
#     get_token = db.query(models_token.Tokens).filter(models_token.Tokens.token == token).first()
#     if get_token is None:
#         raise HTTPException(status_code=404, detail="Token não encontrado")
#     db.delete(get_token)
#     db.commit()
#     return get_token.user_id
#
#
# def password_reset(db: Session, new_password: str, email: str):
#     user = crud_user.get_user_by_email(db=db, email=email)
#     if user is None:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")
#     hashed_password = get_password_hash(new_password)
#     crud_user.update_user_password(db=db, user_id=user.id, password=hashed_password)
#     return user
