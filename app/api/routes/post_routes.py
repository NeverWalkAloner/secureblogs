from typing import Optional

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, DBSession
from app.api.websockets.managers import ws_manager
from app.celery_tasks.workers import encrypt_post_content
from app.core.config import settings
from app.crud import crud_post, crud_user
from app.schemas.post import (
    PaginatedPosts,
    PostBase,
    PostDetails,
    PostInDBBase,
    PostKey,
)


router = APIRouter()


@router.post("/posts/", response_model=PostInDBBase, status_code=201)
async def create_post(
    post: PostBase,
    db: DBSession,
    current_user: CurrentUser,
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


@router.get("/posts/", response_model=PaginatedPosts)
async def get_posts(
    db: DBSession,
    page: int = 1,
    user_group: Optional[int] = None,
):
    posts = await crud_post.get_posts_list(db, page, user_group)
    posts_count = await crud_post.get_posts_count(db, user_group)
    return PaginatedPosts(
        total_count=posts_count, per_page=settings.MAX_PER_PAGE, posts=posts
    )


@router.get("/posts/{post_id}/", response_model=PostDetails)
async def get_post(
    post_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    post = await crud_post.get_post_with_keys(db, post_id, current_user)
    if not post:
        raise HTTPException(status_code=404)
    return post


@router.post("/posts/{post_id}/request_read/", status_code=204)
async def add_read_post_request(
    post_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    post = await crud_post.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404)
    user_key = await crud_user.get_user_key(db, current_user)
    await crud_post.add_read_post_request(db, current_user, post_id)
    await ws_manager.send_personal_message(
        {
            'post_id': post_id,
            'requested_user_id': current_user.id,
            'user_public_key': user_key.public_key,
        },
        post.user_id,
    )


@router.post(
    "/posts/{post_id}/request_read/{request_id}/deny/", status_code=204
)
async def delete_read_post_request(
    post_id: int,
    request_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    await crud_post.delete_read_post_request(db, post_id, request_id)


@router.post(
    "/posts/{post_id}/request_read/{request_id}/accept/", status_code=204
)
async def accept_read_post_request(
    post_id: int,
    request_id: int,
    post_key: PostKey,
    db: DBSession,
    current_user: CurrentUser,
):
    await crud_post.create_post_key(db, post_id, request_id, post_key)
    await crud_post.delete_read_post_request(db, post_id, request_id)
