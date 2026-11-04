from sqlalchemy.orm import Mapped, mapped_column
from database import Base, engine

# ============= 定义模型类（数据库表）=========================

# 定义数据库表对应的模型类


class Todo(Base):                    # Todo 是ORM对象
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(primary_key=True)  # id为主键
    title: Mapped[str]
    done: Mapped[bool] = mapped_column(default=False)
    priority:Mapped[int] = mapped_column(default=1)



# =========== 启动时建表 ============================
Base.metadata.create_all(bind=engine)
