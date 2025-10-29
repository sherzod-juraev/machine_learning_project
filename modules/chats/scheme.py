from pydantic import BaseModel
from uuid import UUID

class ChatResponse(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    title: str


class ChatPost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    title: str