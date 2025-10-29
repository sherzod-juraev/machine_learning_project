from typing import Annotated
from fastapi import APIRouter, status, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from db import get_db
from core import verify_access_token, verify_refresh_token, create_access_token, create_refresh_token, config
from . import crud, UserPost, UserUpdate, UserResponse, TokenResponse


user_router = APIRouter()


@user_router.post(
    '/login',
    summary='Create user',
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse
)
async def create_user(
        response: Response,
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> TokenResponse:
    user_scheme = UserPost(username=user_data.username, password=user_data.password)
    user_db = await crud.create_user(db, user_scheme)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh_token(user_db.id),
        samesite='lax',
        httponly=True,
        path='/',
        secure=False,
        max_age=60 * 60 * 24 * config.REFRESH_TOKEN_DAYS
    )
    token = TokenResponse(
        access_token=create_access_token(user_db.id)
    )
    return token

@user_router.post(
    '/refresh',
    summary='Update tokens',
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse
)
async def update_tokens(
        requuest: Request,
        response: Response
) -> TokenResponse:
    refresh_token = requuest.cookies.get('refresh_token')
    auth_id = verify_refresh_token(refresh_token)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh_token(auth_id),
        samesite='lax',
        httponly=True,
        path='/',
        secure=False,
        max_age=60 * 60 * 24 * config.REFRESH_TOKEN_DAYS
    )
    token = TokenResponse(
        access_token=create_access_token(auth_id)
    )
    return token


@user_router.put(
    '/',
    summary='Full update user',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def full_update(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    user_db = await crud.update_user(db, user_scheme, user_id)
    return user_db


@user_router.patch(
    '/',
    summary='Partial update user',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def partial_update(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    user_db = await crud.update_user(db, user_scheme, user_id, True)
    return user_db

@user_router.get(
    '/',
    summary='Get user',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def get_user(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    user_db = await crud.verify_user(db, user_id)
    return user_db


@user_router.delete(
    '/{user_id}',
    summary='Delete user',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_user(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    user_scheme = UserPost(username=user_data.username, password=user_data.password)
    await crud.delete_user(db, user_scheme, user_id)