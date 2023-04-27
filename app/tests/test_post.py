from unittest import mock

import pytest

from app.core.config import settings


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
