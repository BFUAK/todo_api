from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker



# ============= 数据库引擎配置 ============================
engine = create_engine(
    "sqlite:///./todos.db",           # 数据库文件：todos.db
    connect_args={"check_same_thread" : False}   # SQLite + FastAPI 必备参数
)

# 创建会话工厂
SessionLocal = sessionmaker(bind=engine, autoflush=False)


# 基类
class Base(DeclarativeBase):
    pass



# =================== 依赖：每个请求一个会话，用完关闭 ======================

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db     # 返回数据库会话给路由处理函数， yield 前是"进入"，后是"退出"
    finally:
        db.close()