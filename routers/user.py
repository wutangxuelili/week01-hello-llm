import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from dependencies import get_db, get_password_hash, verify_password
from models import User
from schemas.user import UserCreate

load_dotenv()
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 设置 OAuth2 方案（用于 Swagger 的 Authorize 按钮）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码 token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 查数据库获取用户
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/users")
def get_users(
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    # 查询所有用户
    users = db.query(User).all()
    # 返回列表（FastAPI 会自动将 SQLAlchemy 对象转为字典）
    return users


@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):  # noqa: B008
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    # 创建新用户对象
    new_user = User(username=user.username, password=user.password, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # 刷新获取自增 ID

    # 返回给前端的格式（保持和之前一致）
    return {
        "message": f"欢迎{user.username}注册成功",
        "age_pro": user.age is not None,
        "id": new_user.id,
    }


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),  # noqa: B008
    current_user: User = Depends(get_current_user),  # noqa: B008
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"提示": f"用户{user_id}已删除"}


# 辅助函数
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )  # 将to_encode字典 携带密钥信息 进行加密 转化为一段乱码字符串
    return encoded_jwt


@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):  # noqa: B008
    # 1. 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已被占用")

    # 2. 哈希密码并创建用户
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        username=user_in.username, password=hashed_password, age=user_in.age
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 3. 返回成功信息（不返回密码）
    return {"message": "注册成功", "user_id": new_user.id}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),  # noqa: B008
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/users")
# def get_users(db: dict = Depends(get_db)):
#     return list(db.values())

# @router.get("/users/{user_id}")
# def get_user(user_id: int, db: dict = Depends(get_db)):
#     if user_id not in db:
#         raise HTTPException(status_code=404, detail="User not found")
#     else:
#         return db[user_id]

# @router.post("/users")
# def create_user(
#     user: UserCreate,
#     background_tasks: BackgroundTasks,
#     db: dict = Depends(get_db),
# ):
#     global current_id
#     a = user.model_dump()
#     db[current_id] = a
#     current_id += 1
#     full_name = user.username + "注册成功"

#     background_tasks.add_task(write_log, f"用户 {user.username} 注册成功")  # 写日志
#     return {
#         "message": f"欢迎{full_name}",
#         "age_pro": user.age is not None,
#         "id": f"{current_id - 1}",
#     }

# @router.delete("/users/{user_id}")
# def delete_user(user_id: int, db: dict = Depends(get_db)):
#     if user_id not in db:
#         raise HTTPException(404, "User not found")
#     else:
#         del db[user_id]
#         return {"提示": f"用户{user_id}已删除"}
