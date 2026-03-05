from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from jose import JWTError,jwt
import os,logging
from datetime import datetime,timedelta,timezone

logger=logging.getLogger(__name__)

#là ,je prepare le hacheur pour le hachage
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
TOKEN_EXPIRE=int(os.getenv("ACCES_TOKEN_EXPIRE_MINUTES"))

#je hash le mot de passe
def hash_password(password:str)->str:
    return pwd_context.hash(password[:72])

#je cree un etat de verification de type booleennes
def verify_password(plain:str,hashed:str) ->bool:
    return pwd_context.verify(plain[:72],hashed)

#je cree le token
def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE)
    payload["iat"] = datetime.now(timezone.utc)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

#je le decode , je leve une erreur et j'envoie ca à TokenData dans schemas.py
def decode_token(token: str) -> schemas.TokenData:
    """Vérifie et décode — lève JWTError si invalide ou expiré"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email = payload.get("sub")
    if not email:
        raise JWTError("Token invalide")
    return schemas.TokenData(email=email, role=payload.get("role"))

def get_user_by_email(db:Session,email:str) -> models.User|None:
    return db.query(models.User).filter(models.User.email==email).first()

def create_user(db:Session, user:schemas.UserCreate) ->models.User:
    if get_user_by_email(db,user.email):
        raise ValueError("l'email est deja utilisé")
    db_user=models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Nouveau compte : {user.email}")
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    logger.info(f"Login : {email}")
    return user