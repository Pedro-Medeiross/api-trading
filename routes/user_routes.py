from fastapi import APIRouter
from schemas import user as schemas_user
from schemas import token_data as schemas_token
from sqlalchemy.orm import Session
from connection import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, OAuth2PasswordRequestForm
from cruds import security_crud as security
from cruds import user_crud as crud_user
from datetime import timedelta

user_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get("/me", response_model=schemas_user.User, dependencies=[Depends(security.get_current_user)])
async def read_users_me(current_user: schemas_user.User = Depends(security.get_current_user)):
    """Retorna o usuário logado através do token JWT"""
    return current_user


@user_router.post("/login", response_model=schemas_token.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Loga o usuário e retorna um token JWT"""
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if user:
        access_token_expires = timedelta(hours=security.ACCESS_TOKEN_EXPIRE_HOURS)
        access_token = security.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


@user_router.post('/create', response_model=schemas_user.User)
async def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db),
                      credentials: HTTPBasicCredentials = Depends(security.get_basic_credentials)):
    """Cria um novo usuário"""
    db_user = crud_user.get_user_by_username(db, username=user.username)
    db_email = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        print('teste')
        raise HTTPException(status_code=400, detail="Nome de Usuário já existente!")
    if db_email:
        raise HTTPException(status_code=400, detail="Email já existente!")
    return crud_user.create_user(db=db, user=user)


@user_router.put("/update", response_model=schemas_user.User, dependencies=[Depends(security.get_current_user)])
async def update_user(user: schemas_user.UserUpdate, db: Session = Depends(get_db),
                      current_user: schemas_user.User = Depends(security.get_current_user)):
    """Atualiza os dados do usuário logado"""
    user_id = current_user.id
    if current_user.username != user.username:
        check_username = crud_user.get_user_by_username(db=db, username=user.username)
        if check_username:
            raise HTTPException(status_code=400, detail="Nome de Usuário já está em uso por outra pessoa !")
    if current_user.email != user.email:
        check_email = crud_user.get_user_by_email(db=db, email=user.email)
        if check_email:
            raise HTTPException(status_code=400, detail="Email já está em uso por outra pessoa!")
    return crud_user.update_user(db=db, user=user, user_id=user_id)


@user_router.put("/brokerage/update", response_model=schemas_user.User,
                 dependencies=[Depends(security.get_current_user)])
async def update_user_brokerage(user: schemas_user.UserUpdateBrokerage, db: Session = Depends(get_db),
                                current_user: schemas_user.User = Depends(security.get_current_user)):
    """Atualiza os dados de corretora do usuário logado"""
    user_id = current_user.id
    return crud_user.update_brokerage_credentials(db=db, user=user, user_id=user_id)


@user_router.put("/type", response_model=schemas_user.User,
                 dependencies=[Depends(security.get_current_user)])
async def update_user_account_type(account_type: schemas_user.UserUpdateAccountType, db: Session = Depends(get_db),
                                   current_user: schemas_user.User = Depends(security.get_current_user)):
    """Atualiza o tipo de conta do usuário logado"""
    user_id = current_user.id
    return crud_user.update_user_account_type(db=db, account_type=account_type, user_id=user_id)
