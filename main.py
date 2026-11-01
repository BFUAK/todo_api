
"""
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

# 关闭默认 /docs（引用被墙的 CDN），自定义一个
app = FastAPI(title="Day6 FastAPI 练习", version="0.1.0",
              docs_url=None, redoc_url=None)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/calc/add")
def add(a: int, b: int):
    return {"sum": a + b}


# 自定义 /docs：资源走 unpkg CDN
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )
"""

from fastapi import FastAPI, Path, Query, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse,FileResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from schemas import  TodoCreate
from models import Todo



# ===================6. 路由，注入依赖==============================
app = FastAPI(title="Todo API", version="1.0.0",
              docs_url=None, redoc_url=None)  # 创建 FastAPI实例，未来定义路由、中间件、应用配置都会用到这个实例
"""
# 下面两段代码都是在定义两个接口，访问路径一个是"/", 一个是"/hello/{name}"
@app.get("/")
async def root():  # 由 async关键字修饰的函数会变成异步函数
     return {"message": "Hello World"}
"""

# 创建一条数据存入数据库中
@app.post("/todos",status_code = 201)
def creat_todo(todo:TodoCreate, db:Session = Depends(get_db)):  # db:会话
    db_todo = Todo(**todo.model_dump())   # Pydantic -> ORM
    db.add(db_todo) # 标记增加
    db.commit()    # 提交事务，确认执行，落库  必须调—— 不 commit 数据不会真正落库
    # 此时 db_todo.id 可能已是自增值，但一些数据库默认值（如 created_at）可能还没同步
    db.refresh(db_todo)  # 从数据库重新加载, 让ORM对象拿到数据库生成的 id
    return db_todo    # 完整最新数据

# 查询todo表中所有数据
@app.get("/todos")
def list_todos(db:Session = Depends(get_db)):
    return db.scalars(select(Todo)).all()  # 查询Todo对象，等价于 SELECT * FROM todo



# 按主键从数据库里取一条数据
@app.get("/todos/{todo_id}")
def get_todo(todo_id:int, db:Session=Depends(get_db)):
    todo = db.get(Todo, todo_id)  # 按主键从数据库里取一条数据，数据库里的数据都是Todo类型的
    if not todo:
        raise HTTPException(status_code=404,detail="Todo不存在")
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int,db:Session = Depends(get_db)):
    todo = db.get(Todo,todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo 不存在")
    db.delete(todo)  # 标记删除
    db.commit()   # 提交事务，确认执行，落库
    return {"deleted" : True}



@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


""" 


# 这段代码是一个内存版 Todo API 的
#  "创建 + 列表（带分页参数）+ 单条查询 + 单条查询删除" 四个接口
# 定义类型
class Todo(BaseModel):
    title : str
    done : bool = False
    priority : int = 1

todos = []    # 全局列表，存所有待办，每次重启服务器清空

# 创建一条待办数据，创建成功提示201
@app.post("/todos", status_code=201)
async def creat_todo(todo :Todo):
    new = {"id":len(todos)+1, **todo.model_dump()}  # **todo.model_dump()，在解包，合并为新的字典
    todos.append(new)
    return new

# 分页依赖
async def get_page(page:int = 1, size : int =10):
    return {"page":page,"size":size}


# 分页列出所有待办
@app.get("/todos")
async def list_todos(page_info : dict= Depends(get_page)):
    return {"total":len(todos), **page_info, "data":todos}

# 按id查单条，
# 如果查找到，返回该条数据，如果找不到，报404
@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    for t in todos:
        if t["id"] == todo_id:
            return t
    raise HTTPException(status_code=404,detail="Todo 不存在")

# 按id查找删除，如果删除成功返回{"deleted": "true"}，
# 删除失败报 404
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for t in todos:
        if t["id"] == todo_id:
            todos.remove(t)
            return {"deleted": True}
    raise HTTPException(status_code=404,detail="Todo 不存在")




# 需求：按 id 查询新闻 -> 1-6
@app.get("/news/{id}")
async def get_name(id : int):
    id_list = [1, 2, 3, 4, 5, 6]
    if id not in id_list:
        raise HTTPException(status_code=404, detail="您查找的新闻不存在")  # raise 抛出异常
    return {"id": id }



# 注册：用户名和密码 ->str
# 1. 定义类型
class User(BaseModel):    # 继承基类
    username : str
    password : str

# 2. 使用类型
@app.post("/register")
async def register(user : User):
    return user



@app.get("/")                         # 装饰器声明路由和 HTTP 方法
async def read_root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")          # 路径参数
async def read_item(name: str):
    return {"message": f"Hello {name}"}

@app.get("/calc/add")
async def add(a: int=1, b: int=2):
    return {"sum": a + b}




# 分页参数逻辑共用：新闻列表和用户列表
# 1. 创建依赖项
#    查询参数的增加额外信息用 Query
#    第一页不跳过，大于等于0；每页默认为10条，不超过（小于等于）60条
async def common_parameters(
        skip: int = Query(0, ge=0),
        limit: int = Query(10,le=60)
):
    return {"skip": skip, "limit": limit}

# 3. 声明依赖项 -> 注入依赖
@app.get("/news/new_list")
async def get_news_list(common = Depends(common_parameters)):
    return common

@app.get("/user/user_list")
async def get_user_list(common = Depends(common_parameters)):
    return common



# 需求：新闻接口 -> 响应数据格式 id、title、content
class News(BaseModel):
    id: int
    title: str
    content: str

@app.get("/news/{id}", response_model=News)
async def get_news(id: int):
    return {
        "id": id,
        "title": f"这是第{id}本书",
        "content": "这是一本好书"
    }


@app.get("/file")
async def get_file():
    path ="./files/1.jpg"
    return FileResponse(path)


# 接口 -> 响应 HTML 代码
@app.get("/html",response_class=HTMLResponse)
async def get_html():
    return "<h1>这是一级标题</h1>"


# 需求 查询新闻 -> 分页功能，skip: 跳过的记录数，limit: 返回的记录数 10
# skip 默认为0，要求小于100
@app.get("/news/news_list")
async def get_news_list(
        skip: int = Query(0, description = "跳过的记录数", lt=100),
        limit: int = Query(10, description = "返回的记录数")):
    return {"skip": skip,"limit": limit}


# 访问 /hello 响应结果 msg:你好 FastAPI
@app.get("/hello")
async def get_hello():
    return {"msg": "你好 FastAPI"}


@app.get("/book/{id}")
async def get_book(id: int = Path(..., gt=0, lt=101, description="书籍id,取值范围1-100")):
    return {"id": id, "title": f"这是第{id}本书"}

# 需求：查找书籍的作者，路径参数 name,长度范围 2-10
@app.get("/author/{name}")
async def get_name(name: str = Path(...,min_length=2, max_length=10)):
    return {"msg": f"这是{name}的信息"}
"""
