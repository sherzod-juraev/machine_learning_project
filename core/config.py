from pydantic import BaseModel
from dotenv import load_dotenv
from os import getenv

# enc opening
load_dotenv()

class Config(BaseModel):

    ACCESS_TOKEN_MINUTES: int = int(getenv('ACCESS_TOKEN_MINUTES'))
    REFRESH_TOKEN_DAYS: int = int(getenv('REFRESH_TOKEN_DAYS'))
    ALGORITHM: str = getenv('ALGORITHM')
    SECRET_KEY: str = getenv('SECRET_KEY')
    VITE_API_URL: str = getenv('VITE_API_URL')
    ASYNC_DATABASE_URL: str = getenv('ASYNC_DATABASE_URL')


config = Config()