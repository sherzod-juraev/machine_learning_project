from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core import config

async_engine = create_async_engine(
    url=config.ASYNC_DATABASE_URL,
    pool_size=30,
    max_overflow=60,
    pool_recycle=1800, # db connection time
    pool_timeout=5   # 5 s waiting
)
Async_Session_Local = async_sessionmaker(bind=async_engine)
Base = declarative_base()