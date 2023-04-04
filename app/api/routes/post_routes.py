from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud import crud_post
from app.models.users import User as UserModel
from app.schemas.post import PostBase, PostInDBBase
from app.celery_tasks.workers import encrypt_post_content

router = APIRouter()


@router.post("/posts/", response_model=PostInDBBase, status_code=201)
async def create_post(
    post: PostBase,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    plain_content = post.content
    post.content = ""
    post = await crud_post.create_post(
        db=db,
        post=post,
        author=current_user,
    )
    encrypt_post_content.delay(post_id=post.id, content=plain_content)
    return post
