from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
from database import Base, engine

# =============2. 定义模型类（数据库表）=========================

# 定义数据库表对应的模型类
# Mapped -- 类型注解 （给IDE和SQLalchemy）
# mapped_column -- 声明这是一个数据库列，可带参数
class Todo(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(primary_key=True)  # id为主键
    title: Mapped[str]
    done: Mapped[bool] = mapped_column(default=False)
    priority:Mapped[int] = mapped_column(default=1)



# ===========3. 启动时建表 ============================
Base.metadata.create_all(bind=engine)
