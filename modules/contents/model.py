from datetime import datetime, timezone
from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID as db_uuid
from uuid import UUID, uuid4
from db import Base


class Content(Base):
    __tablename__ = 'contents'

    id: Mapped[UUID] = mapped_column(db_uuid(as_uuid=True), primary_key=True, default=uuid4)
    request: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    chat_id: Mapped[UUID] = mapped_column(db_uuid, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    chat: Mapped['Chat'] = relationship(
        'Chat',
        foreign_keys=[chat_id],
        back_populates='contents',
        lazy='noload'
    )