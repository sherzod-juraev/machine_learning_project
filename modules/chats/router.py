from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from db import get_db
from core import verify_access_token
from . import Chat, ChatPost, ChatResponse, crud



chat_router = APIRouter()


@chat_router.post(
    '/',
    summary='Create chat',
    status_code=status.HTTP_201_CREATED,
    response_model=ChatResponse
)
async def create_chat(
        user_id: Annotated[UUID, Depends(verify_access_token)],
        chat_scheme: ChatPost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Chat:
    chat_db = await crud.create_chat(db, chat_scheme, user_id)
    return chat_db


@chat_router.get(
    '/{chat_id}',
    summary='Get chat',
    status_code=status.HTTP_200_OK,
    response_model=ChatResponse,
    dependencies=[Depends(verify_access_token)]
)
async def get_chat(
        chat_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Chat:
    chat = await crud.verify_chat_by_id(db, chat_id)
    return chat


@chat_router.delete(
    '/{chat_id}',
    summary='Delete chat',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[Depends(verify_access_token)]
)
async def delete_chat(
        chat_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_chat(db, chat_id)