from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
# je recup l'URL de la database dans .env
DATABASE_URL=os.getenv("DATABASE_URL")

#je lance le moteur pour me connecter à la database
engine=create_engine(DATABASE_URL,connect_args={"check_same_thread": False})

#ici j'initie une session avec le moteur engine
LocalSession=sessionmaker(autoflush=False,bind=engine,autocommit=False)

# ici c'est le socle de l'ORM pour ne pas utiliser le SQL
Base=declarative_base()


def get_DB():
    db=LocalSession()
    try:
        yield db
    finally:
        db.close()