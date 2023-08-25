from connection import Base
from sqlalchemy import Column, Integer, Table, ForeignKey

UserRoles = Table('user_roles', Base.metadata,
                  Column('user_id', Integer, ForeignKey('users.id')),
                  Column('role_id', Integer, ForeignKey('roles.id'))
                  )
