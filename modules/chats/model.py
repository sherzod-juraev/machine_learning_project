from datetime import datetime, timezone
from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from uuid import UUID, uuid4
from db import Base


class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[UUID] = mapped_column(db_uuid, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user: Mapped['User'] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='chats',
        lazy='noload'
    )

    contents: Mapped['Content'] = relationship(
        'Content',
        back_populates='chat',
        passive_deletes=True,
        lazy='noload'
    )