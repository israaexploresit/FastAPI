from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status

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


@app.get('/todos')
async def list_books(db: db_dependency):
    return db.query(ToDo).all()


@app.get('/todos/{todo_id}', status_code=status.HTTP_200_OK)
async def get_book(db: db_dependency, todo_id: int = Path(gt=0)):
    response = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if response:
        return response
    raise HTTPException(status_code=404, detail='ToDo not found')
