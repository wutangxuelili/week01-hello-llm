from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# 数据库
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(
        String, nullable=False
    )  # 你的 Pydantic 模型里有 password，所以表里也要有
    age = Column(Integer, nullable=True)  # 可选字段
