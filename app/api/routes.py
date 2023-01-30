from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import crud_user
from app.schemas.user import User, UserCreate

from .deps import get_db

router = APIRouter()


@router.post("/sign-up/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_db = await crud_user.get_user_by_email(db, email=user.email)
    if user_db:
        return user_db
    return await crud_user.create_user(db, user=user)
