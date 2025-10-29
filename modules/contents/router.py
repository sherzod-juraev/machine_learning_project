from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from db import get_db
from . import ContentPost, ContentResponse, ContentUpdate, Content, crud


content_router = APIRouter()


@content_router.post(
    '/',
    summary='Create content',
    status_code=status.HTTP_201_CREATED,
    response_model=ContentResponse
)
async def create_content(
        content_scheme: ContentPost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Content:
    content_scheme.response = 'salom'
    content_db = await crud.create_content(db, content_scheme)
    return content_db


@content_router.put(
    '/{content_id}',
    summary='Full update content',
    status_code=status.HTTP_200_OK,
    response_model=ContentResponse
)
async def full_update(
        content_scheme: ContentUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Content:
    content_scheme.response = 'salom'
    content_db = await crud.update_content(db, content_scheme)
    return content_db


@content_router.get(
    '/{chat_id}',
    summary='All chat contents',
    status_code=status.HTTP_200_OK,
    response_model=list[ContentResponse]
)
async def get_contents(
        chat_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Content]:
    contents = await crud.get_contents_by_chat_id(db, chat_id)
    return contents