from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from fastapi import HTTPException, status
from uuid import UUID
from . import Chat, ChatPost


async def save_chat(
        db: AsyncSession,
        chat_db: Chat,
        /
) -> Chat:
    try:
        await db.commit()
        await db.refresh(chat_db)
        return chat_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'chats_user_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating chat'
        )


async def create_chat(
        db: AsyncSession,
        chat_scheme: ChatPost,
        user_id: UUID,
        /
) -> Chat:
    chat_db = Chat(
        title=chat_scheme.title,
        user_id=user_id
    )
    db.add(chat_db)
    chat_db = await save_chat(db, chat_db)
    return chat_db


async def delete_chat(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> None:
    query = delete(Chat).where(Chat.id == chat_id)
    result = db.execute(query)
    await db.commit()
    if not result.rowcount:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )


async def verify_chat_by_id(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> Chat:
    chat = await db.get(Chat, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found'
        )
    return chat