from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud import crud_user
from app.models.users import User as UserModel
from app.schemas.user import Login, User, UserCreate, UserKey, UserKeyInDB

router = APIRouter()


@router.post("/posts/", response_model=UserKeyInDB)
async def create_post(
    user_key: UserKey,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await crud_user.update_user_key(
        db,
        current_user,
        user_key.public_key,
    )
