from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        name=user.name,
        password=user.password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
