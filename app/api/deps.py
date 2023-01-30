from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal


# Dependency
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
