from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database import get_db
from schemas import TodoCreate, TodoOut, TodoListOut
from models import Todo


# =================== 路由，注入依赖==============================
app = FastAPI(title="Todo API", version="1.0.0",
              docs_url=None, redoc_url=None)  # 创建 FastAPI实例，未来定义路由、中间件、应用配置都会用到这个实例

# 创建一条数据存入数据库中
@app.post("/todos", status_code = 201, response_model=TodoOut)
def creat_todo(todo: TodoCreate, db: Session = Depends(get_db)):  # db:会话
    db_todo = Todo(**todo.model_dump())   # Pydantic -> ORM
    db.add(db_todo)   # 添加到 Session（此时只是被标记为“待插入”，还在内存里）
    db.commit()      # 提交事务（此时才真正生成 INSERT 语句发给数据库）
    db.refresh(db_todo)  # 刷新对象（可选，但强烈推荐。为了拿到数据库自增生成的 id）
    return db_todo    # 完整最新数据, ORM对象 -> response_model -> TodoOut

# 查询todo表中所有数据
@app.get("/todos", response_model=TodoListOut)
def list_todos(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
#    return db.scalars(select(Todo)).all()  # 查询表中所有Todo对象 并提取对象，等价于 SELECT * FROM todo
    total = db.scalar(select(func.count()).select_from(Todo)) or 0
    todos = db.scalars(select(Todo).limit(size).offset((page-1)*size)).all()
    return {
        "total": total,
        "page": page,
        "size": size,
        "data": todos
    }


# 按主键从数据库里取一条数据
@app.get("/todos/{todo_id}")
def get_todo(todo_id:int, db:Session=Depends(get_db)):
    todo = db.get(Todo, todo_id)  # 按主键从数据库里取一条数据，数据库里的数据都是Todo类型的
    if not todo:
        raise HTTPException(status_code=404,detail="Todo不存在")
    return todo

# 按主键从数据库删除一条数据
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int,db:Session = Depends(get_db)):
    todo = db.get(Todo,todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo 不存在")
    db.delete(todo)         # 标记为删除（此时还在内存里，没真正删）
    db.commit()            # 提交事务（真正执行 DELETE 语句）
    return {"deleted" : True}



@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


