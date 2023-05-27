from fastapi import APIRouter

from app.api.deps import CurrentUser, DBSession
from app.crud import crud_user_group
from app.db.base import UserGroup
from app.schemas.user_group import UserGroupBase, UserGroupInDBBase


router = APIRouter()


@router.post(
    "/user_groups/", response_model=UserGroupInDBBase, status_code=201
)
async def create_user_group(
    user_group: UserGroupBase,
    db: DBSession,
    current_user: CurrentUser,
) -> UserGroup:
    user_group_db = await crud_user_group.create_user_group(
        db, user=current_user, user_group=user_group
    )
    return user_group_db


@router.get("/user_groups/", response_model=list[UserGroupInDBBase])
async def get_user_groups_list(
    db: DBSession,
    current_user: CurrentUser,
) -> list[UserGroup]:
    results = await crud_user_group.get_user_groups(db)
    return results


@router.post("/user_groups/{group_id}/", status_code=204)
async def join_group(
    group_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    await crud_user_group.join_user_group(db, current_user, group_id)
