from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.celery.workers import test_task
from app.crud import crud_user_group
from app.db.base import UserGroup
from app.models.users import User as UserModel
from app.schemas.user_group import UserGroupBase, UserGroupInDBBase

router = APIRouter()


@router.post(
    "/user_groups/", response_model=UserGroupInDBBase, status_code=201
)
async def create_user_group(
    user_group: UserGroupBase,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> UserGroup:
    user_group_db = await crud_user_group.create_user_group(
        db, user=current_user, user_group=user_group
    )
    test_task.delay('hello')
    return user_group_db


@router.get("/user_groups/", response_model=list[UserGroupInDBBase])
async def get_user_groups_list(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
) -> list[UserGroup]:
    results = await crud_user_group.get_user_groups(db)
    return results