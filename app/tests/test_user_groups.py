import pytest
from sqlalchemy import func, select

from app.models.users import UserGroupAssociation


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
async def test_create_group_success(async_client, user, token):
    request_data = {"name": "common group"}
    response = await async_client.post(
        "/user_groups/",
        json=request_data,
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["name"] == "common group"


@pytest.mark.asyncio
async def test_join_user_groups_success(
    async_client, user_group, token, db_session
):
    response = await async_client.post(
        f"/user_groups/{user_group.id}/",
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 204
    users_in_group = await db_session.execute(
        select(func.count(UserGroupAssociation.id))
    )
    assert users_in_group.scalar_one() == 1
