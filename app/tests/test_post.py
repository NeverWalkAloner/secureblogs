from unittest import mock

import pytest


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
