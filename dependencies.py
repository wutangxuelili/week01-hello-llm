from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

import redis

redis_client = redis.Redis(
    host="localhost", port=6379, decode_responses=True, protocol=2
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# fake_db = {}
# current_id = 1


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def write_log(a: str):  # 写入字符串
    with open("server.log", "a", encoding="utf-8") as f:
        f.write(a)
