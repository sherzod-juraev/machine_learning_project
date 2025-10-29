from fastapi import APIRouter, Depends
from core import tags, prefixes, verify_access_token

# import models
from .users.model import User
from .chats.model import Chat
from .contents.model import Content

__all__ = ['User', 'Chat', 'Content']

# import routers
from .users.router import user_router
from .chats.router import chat_router
from .contents.router import content_router


api_router = APIRouter()

api_router.include_router(
    user_router,
    prefix=prefixes.users,
    tags=[tags.users]
)
api_router.include_router(
    chat_router,
    prefix=prefixes.chats,
    tags=[tags.chats]
)
api_router.include_router(
    content_router,
    prefix=prefixes.contents,
    tags=[tags.contents],
    dependencies=[Depends(verify_access_token)]
)