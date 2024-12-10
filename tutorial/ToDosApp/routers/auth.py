from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status
from jose import jwt, JWTError

from models import User
from database import SessionLocal

router = APIRouter()

'''
For password hashing:
pip install passlib bcrypt==4.0.1
'''

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

'''
For JWT Encoding:
pip install "python-jose[cryptography]"
'''

SECRET_KEY = '4c9131431e44e8b0a46750919a50db10ab2b149f77f7df790da4acc80bac10f4'
ALGORITHM = 'HS256'

oauth2bearer = OAuth2PasswordBearer(tokenUrl='token')

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


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username, password, db):
    user_query = db.query(User).filter(User.username == username).first()
    if not user_query:
        return False
    if not bcrypt_context.verify(password, user_query.hashed_password):
        return False
    return user_query


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


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


async def get_current_user(token: Annotated[str, Depends(oauth2bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Invalid credentials')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid credentials')


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(
                db: db_dependency,
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return {'mesaage': 'Failed authentication'}

    token = create_access_token(user.username, user.id, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}
