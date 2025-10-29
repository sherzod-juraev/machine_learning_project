from pydantic import BaseModel


class Prefix(BaseModel):

    users: str = '/auth'
    chats: str = '/chats'
    contents: str = '/content'


prefixes = Prefix()