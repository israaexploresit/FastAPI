from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel

from database import SessionLocal
from models import User
from routers.auth import get_current_user
from routers.auth import bcrypt_context

router = APIRouter(
    prefix='/user',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class PasswordRequest(BaseModel):
    current_password: str
    password: str


@router.get('/info/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency,
                   db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Not Authorized')
    user_id = user.get('id')
    user_obj = db.query(User).filter(User.id == user_id)
    if not user_obj.first():
        raise HTTPException(status_code=404, detail='User not found')
    return user_obj.all()


@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency,
                          db: db_dependency,
                          request_data: PasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Not Authorized')
    user_id = user.get('id')
    user_obj = db.query(User).filter(User.id == user_id).first()
    password = request_data.password
    confirm_password = request_data.confirm_password
    if password != confirm_password:
        raise HTTPException(status_code=400,
                            detail='Password and confirm password does not match')
    if not user_obj:
        raise HTTPException(status_code=404, detail='User not found')

    user_obj.hashed_password = bcrypt_context.hash(request_data.password)
    db.add(user_obj)
    db.commit()
