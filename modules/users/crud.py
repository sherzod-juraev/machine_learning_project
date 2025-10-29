from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete
from fastapi import HTTPException, status
from uuid import UUID
from core import hashed_password, create_access_token
from core import verify_plain_password
from . import User, UserUpdate, UserPost


async def save_user_to_db(
        db: AsyncSession,
        user_db: User,
        /
) -> User:
    try:
        await db.commit()
        await db.refresh(user_db)
        return user_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'ix_users_username' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating user'
        )


async def create_user(
        db: AsyncSession,
        user_scheme: UserPost,
        /
) -> User:
    user_db = User(
        username=user_scheme.username,
        password=hashed_password(user_scheme.password)
    )
    db.add(user_db)
    user_db = await save_user_to_db(db, user_db)
    return user_db


async def update_user(
        db: AsyncSession,
        user_scheme: UserUpdate,
        user_id: UUID,
        exclude_unset: bool = False,
        /
) -> User:
    user_db = await verify_user(db, user_id)
    for field, value in user_scheme.model_dump(exclude_unset=exclude_unset).items():
        if field == 'image_url':
            setattr(user_db, field, str(value))
        else:
            setattr(user_db, field, value)
    user_db = await save_user_to_db(db, user_db)
    return user_db


async def delete_user(
        db: AsyncSession,
        user_scheme: UserPost,
        user_id: UUID,
        /
) -> None:
    user_db = await verify_user(db, user_id)
    await verify_username_and_password(user_db, user_scheme)
    query = delete(User).where(User.id == user_id)
    try:
        result = await db.execute(query)
        await db.commit()
        if not result.rowcount:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot delete user'
        )


async def verify_username_and_password(
        user_db: User,
        user_scheme: UserPost,
        /
) -> None:
    if user_db.username != user_scheme.username and not verify_plain_password(user_scheme.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username and password are wrong'
        )
    elif user_db.username != user_scheme.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username is wrong'
        )
    elif not verify_plain_password(user_scheme.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password is wrong'
        )


async def verify_user(
        db: AsyncSession,
        user_id: UUID,
        /
) -> User:
    user_db = await db.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user_db