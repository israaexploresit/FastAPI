from passlib.context import CryptContext
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

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


def authenticate_user(username, password, db):
    user_query = db.query(User).filter(User.username == username).first()
    if not user_query:
        return False
    if not bcrypt_context.verify(password, user_query.hashed_password):
        return False
    return True


@router.post('/auth/', status_code=status.HTTP_201_CREATED)
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


@router.post('/login', status_code=status.HTTP_200_OK)
async def login_for_access_token(
                db: db_dependency,
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_authenticated = authenticate_user(form_data.username,
                                           form_data.password, db)
    if not user_authenticated:
        return {'mesaage': 'Failed authentication'}
    return {'message': 'Successful authentication'}
