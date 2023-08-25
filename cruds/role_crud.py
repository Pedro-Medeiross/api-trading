from typing import Optional
from sqlalchemy.orm import Session
from models import role as models_role
from schemas import roles as schemas_role
from cruds import user_crud as user_crud


def get_role_by_name(db: Session, name: str) -> Optional[models_role.Role]:
    role = db.query(models_role.Role).filter(models_role.Role.name == name).first()
    return role


def create_role(db: Session, role: schemas_role.RoleCreate):
    db_role = models_role.Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def has_role(db: Session, user_id: int, role_name: str) -> bool:
    user = user_crud.get_user_by_id(db, user_id)
    for role in user.roles:
        if role.name == role_name:
            return True
    return False
