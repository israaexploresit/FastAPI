from passlib.context import CryptContext
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session

from models import User
from database import SessionLocal

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    password: str


@router.post('/auth/')
async def create_user(
                db: db_dependency,
                request_data: CreateUserRequest):
    user_obj = User(
        username=request_data.username,
        email=request_data.email,
        first_name=request_data.first_name,
        last_name=request_data.last_name,
        role=request_data.role,
        hashed_password=bcrypt_context.hash(request_data.password)
    )
    db.add(user_obj)
    db.commit()
    return user_obj
