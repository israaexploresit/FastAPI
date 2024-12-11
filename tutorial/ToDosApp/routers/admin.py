from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from database import SessionLocal
from models import ToDo
from routers.auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/todos/', status_code=status.HTTP_200_OK)
async def list_all_todos(user: user_dependency,
                         db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Not Authorized')
    return db.query(ToDo).all()


@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency,
                      todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Not Authorized')
    todo_objs = db.query(ToDo).filter(ToDo.id == todo_id)
    if not todo_objs.first():
        raise HTTPException(status_code=404, detail='ToDo not found')
    todo_objs.delete()
    db.commit()
