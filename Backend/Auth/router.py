from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_DB
from . import schemas, service
from jose import JWTError

router=APIRouter(prefix="/auth",tags=["authentification"])
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=schemas.UserOut)
def register(user_data:schemas.UserCreate,db:Session=Depends(get_DB)):
    try:
        return service.create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login",response_model=schemas.Token)
def login(credentials:schemas.UserLogin,db:Session=Depends(get_DB)):
    user = service.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Identifiants incorrects",
    headers={"WWW-Authenticate": "Bearer"},
    )
    token = service.create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_DB)):
    try:
        token_data = service.decode_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")
    user = service.get_user_by_email(db, token_data.email)
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user