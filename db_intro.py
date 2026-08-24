import sqlite3

# 1. 连接数据库（如果文件不存在，它会自动创建）
conn = sqlite3.connect("practice.db")

# 2. 创建一个“游标（Cursor）”，它是执行 SQL 语句的“手”
cursor = conn.cursor()

print("数据库连接成功！")

# --- 清空旧表（重建结构） ---
# cursor.execute("DROP TABLE IF EXISTS todos")  # 先删子表（依赖方）
# cursor.execute("DROP TABLE IF EXISTS users")  # 再删主表
# conn.commit()
# print("旧表已删除，准备重建")
# 执行创建表的 SQL 语句
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
# cursor.execute("INSERT INTO users(username) VALUES('李哥')")
# user_id = cursor.lastrowid
# print(f"创建用户成功，用户ID为: {user_id}")

# cursor.execute("INSERT INTO todos(title,user_id) VALUES('写作业',?)", (user_id,))
# cursor.execute("INSERT INTO todos (title, user_id) VALUES ('买牛奶', ?)", (user_id,))
# conn.commit()
# print("两条待办插入成功")
# 提交更改（让数据库真正执行）
cursor.execute("""
SELECT users.username, todos.title, todos.completed
FROM todos
JOIN users ON todos.user_id = users.id
""")

rows = cursor.fetchall()

print("当前所有待办事项及其所属用户：")
for row in rows:
    status = "已完成" if row[2] == 1 else "未完成"
    print(f"用户: {row[0]}, 任务: {row[1]}, 状态: {status}")

conn.commit()
print("1")

# --- 增（INSERT）：插入三条学生记录 ---
# cursor.execute("INSERT INTO students (name, age, score) VALUES ('张三', 18, 95.5)")

# conn.commit()
# print("3 条数据插入成功")

# 改
# cursor.execute("UPDATE students SET age=1 WHERE name='张三'")
# conn.commit()
# 删除
# cursor.execute("DELETE FROM students ")
# conn.commit()
# --- 查（SELECT）：取出所有数据验证 ---
# cursor.execute("SELECT * FROM students")
# rows = cursor.fetchall()

# print("当前数据库里的学生列表：")
# for row in rows:
#     print(f"ID: {row[0]}, 姓名: {row[1]}, 年龄: {row[2]}, 分数: {row[3]}")
