from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_404_NOT_FOUND

from app import messages
from database import User
from database import get_db
from database.schemas import UserGet
from database.schemas import UserPost

api_v1_users = APIRouter()


@api_v1_users.post('/', response_model=UserGet, status_code=HTTP_201_CREATED)
def post_user(
        *,
        db_session: Session = Depends(get_db),
        data: UserPost
) -> UserGet:
    if User.get_user_by_name(db_session=db_session, name=data.name) is not None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=messages.USER_NAME_ALREADY_EXISTS)

    if User.get_user_by_email(db_session=db_session, email=data.email) is not None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=messages.USER_EMAIL_ALREADY_EXISTS)

    return User.create(db_session=db_session, data=data)


@api_v1_users.get('/', response_model=List[UserGet], status_code=HTTP_200_OK)
def get_users(
        db_session: Session = Depends(get_db)
) -> UserGet:
    return User.get_users(db_session=db_session)


@api_v1_users.get('/{name}/', response_model=UserGet, status_code=HTTP_200_OK)
def get_user_name(
        *,
        db_session: Session = Depends(get_db),
        name: str
) -> UserGet:
    user = User.get_user_by_name(db_session=db_session, name=name)

    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)

    return user
