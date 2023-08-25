from fastapi import APIRouter
from schemas import management as schemas_management
from sqlalchemy.orm import Session
from connection import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from cruds import security_crud as security
from cruds import management_crud as management_crud
from cruds import user_crud as crud_user
from schemas import user as schemas_user

management_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@management_router.get("/user/values", response_model=schemas_management.Management,
                       dependencies=[Depends(security.get_current_user)])
async def get_management_by_user(db: Session = Depends(get_db),
                                 current_user: schemas_user.User = Depends(security.get_current_user)):
    """Retorna o gerenciamento de um usuário"""
    db_user = crud_user.get_user_by_id(db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return management_crud.get_management_by_user(db, user_id=current_user.id)


@management_router.put("/update/user/values", response_model=schemas_management.Management,
                       dependencies=[Depends(security.get_current_user)])
async def update_management(management: schemas_management.ManagementUpdate,
                            db: Session = Depends(get_db),
                            current_user: schemas_user.User = Depends(security.get_current_user)):
    """Atualiza o gerenciamento de um usuário"""
    db_user = crud_user.get_user_by_id(db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return management_crud.update_management(db=db, management=management, user_id=current_user.id)
