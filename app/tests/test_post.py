import pytest
from sqlalchemy import func, select

from app.core.config import settings
from app.db.base import ReadPostRequest


@pytest.mark.asyncio
async def test_create_post_success(async_client, user, user_group, token):
    request_data = {
        "title": "hello",
        "content": "hello world",
        "group_id": user_group.id,
    }
    response = await async_client.post(
        "/posts/",
        json=request_data,
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["title"] == "hello"
    assert response.json()["group_id"] == user_group.id
    assert response.json()["content"] == ""  # hidden


@pytest.mark.asyncio
async def test_posts_list_success(async_client, posts, token):
    response = await async_client.get(
        "/posts/",
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == len(posts)
    assert data["per_page"] == settings.MAX_PER_PAGE
    assert len(data["posts"]) == len(posts)
    for indx, post in enumerate(data["posts"]):
        assert post["title"] == posts[indx].title
        assert post["content"] == posts[indx].content
        assert post["group_id"] == posts[indx].group_id
        assert post["id"] == posts[indx].id


@pytest.mark.asyncio
async def test_post_details_success(async_client, posts, post_keys, token):
    post_db = posts[0]
    response = await async_client.get(
        f"/posts/{post_db.id}/",
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 200
    post = response.json()
    assert post["title"] == post_db.title
    assert post["content"] == post_db.content
    assert post["group_id"] == post_db.group_id
    assert post["id"] == post_db.id
    assert len(post["keys"]) == 1
    assert post["keys"][0]["encrypted_key"] == post_keys[0].encrypted_key


@pytest.mark.asyncio
async def test_request_post_read_success(
    async_client, db_session, posts, user, user_key, token
):
    post_db = posts[0]
    response = await async_client.post(
        f"/posts/{post_db.id}/request_read/",
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 204
    users_in_group = await db_session.execute(
        select(func.count(ReadPostRequest.id)).where(
            ReadPostRequest.user_id == user.id
        )
    )
    assert users_in_group.scalar_one() == 1


@pytest.mark.asyncio
async def test_deny_read_post_request_success(
    async_client, db_session, posts, token, read_post_requests
):
    post_db = posts[0]
    users_in_group = await db_session.execute(
        select(func.count(ReadPostRequest.id)).where(
            ReadPostRequest.post_id == post_db.id
        )
    )
    assert users_in_group.scalar_one() == 1
    response = await async_client.post(
        f"/posts/{post_db.id}/request_read/{read_post_requests[0].id}/deny/",
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 204
    users_in_group = await db_session.execute(
        select(func.count(ReadPostRequest.id)).where(
            ReadPostRequest.post_id == post_db.id
        )
    )
    assert users_in_group.scalar_one() == 0
