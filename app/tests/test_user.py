import pytest
from app.models.users import UserToken
from sqlalchemy import select


@pytest.mark.asyncio
async def test_sign_up(async_client):
    request_data = {
        "email": "hello@world.com",
        "name": "Alex",
        "password": "12345678",
    }
    response = await async_client.post("/sign-up/", json=request_data)
    assert response.status_code == 200
    assert response.json()["id"] is not None
    assert response.json()["email"] == "hello@world.com"
    assert response.json()["name"] == "Alex"
    assert response.json()["token"]["access_token"] is not None
    assert response.json()["token"]["expires"] is not None
    assert response.json()["token"]["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_sign_up_existing_user(async_client, user):
    request_data = {
        "email": user.email,
        "name": "Alex",
        "password": "12345678",
    }
    response = await async_client.post("/sign-up/", json=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User already registered"


@pytest.mark.asyncio
async def test_sign_up_weak_password(async_client):
    request_data = {
        "email": "hello@world.com",
        "name": "Alex",
        "password": "123",
    }
    response = await async_client.post("/sign-up/", json=request_data)
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "ensure this value has at least 8 characters"
    )
    assert (
        response.json()["detail"][0]["type"]
        == "value_error.any_str.min_length"
    )
