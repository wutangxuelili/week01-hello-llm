from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    age: int | None = None


class UserLogin(BaseModel):
    username: str
    password: str
