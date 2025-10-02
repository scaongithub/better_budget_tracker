from __future__ import annotations

from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from . import crud
from .database import get_session
from .models import User
from .schemas import Token, UserRead
from .security import ACCESS_TOKEN_EXPIRE_MINUTES, TokenStore, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
_token_store = TokenStore()


async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Token:
    user = crud.get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _token_store.create_token(user.id, access_token_expires)
    return Token(access_token=access_token)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    user_id = _token_store.get_user_id(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.from_orm(current_user)
