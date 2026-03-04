from sqlalchemy import column, String, Integer,DateTime,Boolean
from sqlalchemy.sql import func
from database import Base

#ici, je cree la table Utilisateur pour ma DB en evitant de taper du sql avec sqlalchemy
class User():
    __tablename__="users"

    id=column(Integer,primary_key=True, indedx=True)
    email=column(String(255),unique=True,index=True,nullable=False)
    hashed_password=column(String(60),nullable=False)
    is_active=column(Boolean,default=True,nullable=False)
    role=column(String(50),default="user", nullable=False)

    created_at=column(DateTime(timezone=True),server_default=func.now)
    updated_at=column(DateTime(timezone=True),on_update=func.now)
    last_login=column(DateTime(timezone=True),nullable=True)
