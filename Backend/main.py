import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine, Base
from Auth.router import router as auth_router
from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv("ENV")

logging.basicConfig(
level=logging.DEBUG if ENV == "development" else logging.INFO,
format="%(asctime)s - %(levelname)s - %(message)s"
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth System API")
app.include_router(auth_router)

