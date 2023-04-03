import pytest
from unittest import mock


@pytest.mark.asyncio
async def test_user_groups_success(async_client, user, user_group, token):
    response = await async_client.get(
        "/user_groups/",
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == user_group.id
    assert response.json()[0]["name"] == user_group.name


@pytest.mark.asyncio
@mock.patch('app.api.routes.user_group_routes.create_user_key.delay')
async def test_create_group_success(mock_task, async_client, user, token):
    request_data = {"name": "common group"}
    response = await async_client.post(
        "/user_groups/",
        json=request_data,
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["name"] == "common group"
