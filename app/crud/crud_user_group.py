from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import User, UserGroup, UserGroupAssociation
from app.schemas.user_group import UserGroupBase


async def create_user_group(
    db: AsyncSession, user: User, user_group: UserGroupBase
) -> UserGroup:
    db_user_group = UserGroup(
        name=user_group.name,
    )
    db_user_group.users.append(user)
    db.add(db_user_group)
    await db.commit()
    await db.refresh(db_user_group)
    return db_user_group


async def get_user_groups(db: AsyncSession) -> list[UserGroup]:
    result = await db.execute(select(UserGroup))
    return result.scalars().all()


async def join_user_group(db: AsyncSession, user: User, group_id: int) -> None:
    exists_statement = select(UserGroupAssociation.id).where(
        (UserGroupAssociation.user_id == user.id)
        & (UserGroupAssociation.group_id == group_id)
    )
    result = await db.execute(exists_statement)
    if result.scalars().first():
        return None
    db_user_group_association = UserGroupAssociation(
        user_id=user.id,
        group_id=group_id,
    )
    db.add(db_user_group_association)
    await db.commit()
