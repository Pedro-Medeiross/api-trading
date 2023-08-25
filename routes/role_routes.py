from fastapi import APIRouter
from schemas import roles as schemas_roles
from schemas import user as schemas_user
from sqlalchemy.orm import Session
from connection import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from cruds import security_crud as security
from cruds import role_crud as crud_role

role_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@role_router.get("/name", response_model=schemas_roles.Role, dependencies=[Depends(security.get_current_user)])
async def get_role_by_name(name: schemas_roles.GetRoleName, db: Session = Depends(get_db),
                           current_user: schemas_user.User = Depends(security.get_current_user)):
    """Retorna uma role pelo nome"""
    db_role = crud_role.get_role_by_name(db, name=name.name)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role não encontrado")
    return db_role


@role_router.post("/create", response_model=schemas_roles.Role, dependencies=[Depends(security.get_current_user)])
async def create_role(role: schemas_roles.RoleCreate, db: Session = Depends(get_db),
                      current_user: schemas_user.User = Depends(security.get_current_user)):
    """Cria uma role"""
    if not crud_role.has_role(db=db, user_id=current_user.id, role_name='admin'):
        raise HTTPException(status_code=403, detail="Acesso negado")
    db_role = crud_role.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role já existe")
    return crud_role.create_role(db=db, role=role)
