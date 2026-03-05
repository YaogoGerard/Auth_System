from sqlalchemy import Column, String, Integer,DateTime,Boolean
from sqlalchemy.sql import func
from database import Base

#ici, je cree la table Utilisateur pour ma DB en evitant de taper du sql avec sqlalchemy
class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, index=True)
    username=Column(String(255),index=True,nullable=False)
    email=Column(String(255),unique=True,index=True,nullable=False)
    hashed_password=Column(String(60),nullable=False)
    is_active=Column(Boolean,default=True,nullable=False)
    role=Column(String(50),default="user", nullable=False)

    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())
    last_login=Column(DateTime(timezone=True),nullable=True)
