from pydantic import BaseModel
from uuid import UUID


class ContentResponse(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    request: str
    response: str


class ContentPost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    request: str
    response: str | None = None
    chat_id: UUID


class ContentUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    request: str
    response: str | None = None