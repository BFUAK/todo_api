# 项目名称
Todo API

## 项目简介
基于 FastAPI + SQLAlchemy + SQLite 实现的待办事项API

## 功能特性
实现的接口：

| 请求方法  |  URL路径 | 处理函数  |  功能 |
|---|---|---|---|
| POST  |/todos    |  creat_todo  | 创建一条待办事项  |
|  GET |  /todos | list_todos  | 分页列出待办事项|
| GET   | /todos/{todo_id}  | get_todo   | 根据todo_id查询待单条办事项  |
| DELETE   |  /todos/{todo_id} |  delete_todo | 根据todo_id删除待单条办事项  |

支持增删查操作，操作落库            
自动生成可交互文档

## 项目结构
main.py        --- 路由层             
database.py    --- 数据库配置             
models.py      --- ORM模型          
schemas.py     --- Pydantic校验

## 接口文档链接
http://127.0.0.1:8000/docs

## 环境要求
Python 3.12             
FastAPI（Web框架）         
SQLAlchemy（ORM）       
SQLite（数据库）

## 快速开始
pip install -r requirements.txt                                                     
uvicorn main:app --reload
