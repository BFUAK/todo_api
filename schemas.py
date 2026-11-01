from pydantic import BaseModel



#  ====================4. Pydantic模型（自定义数据格式）======================
class TodoCreate(BaseModel):
    title: str
    done: bool
    priority: int