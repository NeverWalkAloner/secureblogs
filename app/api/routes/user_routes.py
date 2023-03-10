from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud import crud_user
from app.models.users import User as UserModel
from app.schemas.user import Login, User, UserCreate, UserKey, UserKeyInDB

router = APIRouter()


@router.post("/sign-up/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_db = await crud_user.get_user_by_email(db, email=user.email)
    if user_db:
        raise HTTPException(status_code=400, detail="User already registered")
    user = await crud_user.create_user(db, user=user)
    user.token = await crud_user.create_user_token(db, user=user)
    return user


@router.post("/login/", response_model=User)
async def login(user: Login, db: AsyncSession = Depends(get_db)):
    user_db = await crud_user.get_user_by_email(db, email=user.email)
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found")
    if user_db.password != user.password:
        raise HTTPException(status_code=400, detail="User not found")
    user_db.token = await crud_user.create_user_token(db, user=user_db)
    return user_db


@router.get("/users/me/", response_model=User)
async def me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.post("/users/me/public_key/", response_model=UserKeyInDB)
async def update_public_key(
    user_key: UserKey,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await crud_user.update_user_key(
        db,
        current_user,
        user_key.public_key,
    )
