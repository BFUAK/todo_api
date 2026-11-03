from pydantic import BaseModel, ConfigDict


#  ==================== Pydantic模型（自定义数据格式）======================
# TodoCreate 是Pydantic 实例对象
class TodoCreate(BaseModel):
    title: str
    done: bool = False
    priority: int = 1


class TodoOut(BaseModel):
    id: int
    title: str
    done: bool
    priority: int
    model_config = ConfigDict(from_attributes=True)  # 允许从 ORM 对象直接取值

class TodoListOut(BaseModel):
    total: int
    page: int
    size: int
    data: list[TodoOut]