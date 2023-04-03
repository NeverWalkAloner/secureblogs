from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)

sync_engine = create_engine(settings.SYNC_SQLALCHEMY_DATABASE_URL, echo=True)
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)
