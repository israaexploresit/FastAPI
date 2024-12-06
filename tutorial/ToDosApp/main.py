from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends

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


@app.get('/books')
async def list_books(db: db_dependency):
    return db.query(ToDo).all()
