from pydantic import BaseModel, EmailStr,Field,field_validator
from typing import Optional
from datetime import datetime
import re

#ici , c'est pour structure les donnees que notre front-end va envoyer et pouvoir bien les recevoir
# ici, c'est aussi le typage des donnees que front envoie 
class UserCreate(BaseModel):
    username:str=Field(min_length=3)
    email:EmailStr
    password:str=Field(min_length=8,max_length=72)
    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Le mot de passe doit contenir une majuscule")
        if not re.search(r"[0-9]", v):
            raise ValueError("Le mot de passe doit contenir un chiffre")
        return v
    

class UserOut(BaseModel):
        id:int
        username: str
        email:EmailStr
        is_active:bool
        role:str
        created_at:datetime

        class Config:
            from_attributes=True

class UserLogin(BaseModel):
        email: str 
        password:str
        
class Token(BaseModel):
            access_token:str
            token_type:str = "bearer"

class TokenData(BaseModel):
            email:Optional[str]=None
            role:Optional[str]=None