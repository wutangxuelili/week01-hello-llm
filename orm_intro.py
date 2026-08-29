from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine, text
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=True)

    todos = relationship("Todo", back_populates="user")


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="todos")


engine = create_engine("sqlite:///practice.db", echo=True)

Base.metadata.create_all(engine)

print("orm完成")

session = Session(engine)
session.execute(text("DELETE FROM todos"))
session.execute(text("DELETE FROM users"))
session.commit()
print("已清空旧数据")

user1 = User(username="赵6")
task1 = Todo(title="学习1")
task2 = Todo(title="写代码1")

user1.todos.append(task1)
user1.todos.append(task2)

session.add(user1)

session.commit()

print("数据持久化成功")
print(f"用户id:{user1.id},任务:{len(user1.todos)}")


from sqlalchemy import select

stmt = select(User).where(User.username == "赵6")
user_from_db = session.execute(stmt).scalar_one()

print(f"yonghu{user_from_db.username}")

# 修改
first_task = user_from_db.todos[0]
first_task.title = "xuexi gaojitexing"

session.commit()
print("gengxinwancheng")

# --- 删除：移除用户赵六的第一个待办 ---
# 先获取赵六的用户对象（如果前面已经查询过 user_from_db，可以直接复用）
user_from_db = session.execute(select(User).where(User.username == "赵6")).scalar_one()

# 取出第一个待办（即 "xuexi gaojitexing"）
task_to_delete = user_from_db.todos[0]

# 执行删除（标记为待删除）
session.delete(task_to_delete)

# 提交事务（真正删除）
session.commit()

print("已删除第一个待办")

# 再次刷新用户对象，确认列表已更新
session.refresh(user_from_db)
print(f"剩余待办数: {len(user_from_db.todos)}")
for t in user_from_db.todos:
    print(f"  - {t.title}")

# 关闭会话
session.close()
