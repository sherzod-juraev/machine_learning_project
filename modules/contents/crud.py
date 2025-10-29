from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from . import Content, ContentPost
from uuid import UUID
from fastapi import HTTPException, status


async def save_content(
        db: AsyncSession,
        content_db: Content,
        /
) -> Content:
    try:
        await db.commit()
        await db.refresh(content_db)
        return content_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'contents_chat_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Chat not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating content'
        )


async def create_content(
        db: AsyncSession,
        content_scheme: ContentPost,
        /
) -> Content:
    content_db = Content(
        request=content_scheme.request,
        response=content_scheme.response,
        chat_id=content_scheme.chat_id
    )
    db.add(content_db)
    content_db = await save_content(db, content_db)
    return content_db


async def update_content(
        db: AsyncSession,
        content_scheme: ContentPost,
        content_id: UUID,
        exclude_unset: bool = False,
        /
) -> Content:
    content_db = await verify_content(db, content_id)
    for field, value in content_scheme.model_dump(exclude_unset=exclude_unset).items():
        setattr(content_db, field, value)
    content_db = await save_content(db, content_db)
    return content_db


async def verify_content(
        db: AsyncSession,
        content_id: UUID,
        /
) -> Content:
    content_db = await db.get(Content, content_id)
    if not content_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Content not found'
        )
    return content_db


async def get_contents_by_chat_id(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> list[Content]:
    query = select(Content).where(Content.chat_id == chat_id).order_by(Content.created_at.asc())
    result = await db.execute(query)
    contents = result.scalars().all()
    if not contents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Contents not found'
        )
    return contents