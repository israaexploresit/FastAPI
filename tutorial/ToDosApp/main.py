from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field

from database import engine, SessionLocal
from models import ToDo
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class ToDoData(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0)
    is_completed: bool = Field(default=False)


@app.get('/todos')
async def list_todos(db: db_dependency):
    return db.query(ToDo).all()


@app.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    response = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if response:
        return response
    raise HTTPException(status_code=404, detail='ToDo not found')


@app.post('/todos', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, request_data: ToDoData):
    todo_obj = ToDo(**request_data.model_dump())
    db.add(todo_obj)
    db.commit()


@app.put('/todos/{todo_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,
                      request_data: ToDoData,
                      todo_id: int = Path(gt=0)):
    todo_obj = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail='ToDo not found')
    todo_obj.title = request_data.title
    todo_obj.description = request_data.description
    todo_obj.priority = request_data.priority
    todo_obj.is_completed = request_data.is_completed
    db.add(todo_obj)
    db.commit()


@app.delete('/todos/{todo_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency,
                      todo_id: int = Path(gt=0)):
    todo_objs = db.query(ToDo).filter(ToDo.id == todo_id)
    if not todo_objs.first():
        raise HTTPException(status_code=404, detail='ToDo not found')
    todo_objs.delete()
    db.commit()
