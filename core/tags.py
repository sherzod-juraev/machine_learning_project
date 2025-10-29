from pydantic import BaseModel


class Tags(BaseModel):

    users: str = 'Authenticate'
    chats: str = 'Chats'
    contents: str = 'Contents'


tags = Tags()