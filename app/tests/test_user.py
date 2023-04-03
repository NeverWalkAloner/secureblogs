import pytest
from sqlalchemy import func, select

from app.models.users import UserKeys, UserToken


@pytest.mark.asyncio
async def test_sign_up(async_client, db_session):
    request_data = {
        "email": "hello@world.com",
        "name": "Alex",
        "password": "12345678",
    }
    response = await async_client.post("/sign-up/", json=request_data)
    token_counts = await db_session.execute(select(func.count(UserToken.id)))
    assert token_counts.scalar_one() == 1
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


@pytest.mark.asyncio
async def test_login_success(async_client, user):
    request_data = {
        "email": user.email,
        "password": "12345678",
    }
    response = await async_client.post("/login/", json=request_data)
    assert response.status_code == 200
    assert response.json()["email"] == user.email
    assert response.json()["name"] == user.name
    assert response.json()["token"]["access_token"] is not None
    assert response.json()["token"]["expires"] is not None
    assert response.json()["token"]["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_email(async_client, user):
    request_data = {
        "email": "invalid@mail.com",
        "password": "12345678",
    }
    response = await async_client.post("/login/", json=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_login_invalid_password(async_client, user):
    request_data = {
        "email": user.email,
        "password": "password123",
    }
    response = await async_client.post("/login/", json=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_user_details_success(async_client, user, token):
    response = await async_client.get(
        "/users/me/", headers={"Authorization": f"Bearer {token.token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == user.email
    assert response.json()["name"] == user.name


@pytest.mark.asyncio
async def test_user_details_unauthorized(async_client, user):
    response = await async_client.get("/users/me/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_upgrade_public_key(async_client, db_session, token):
    request_data = {
        "public_key": "-----BEGIN PUBLIC KEY-----"
        "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkvRE10cEjZxHg80ckA4h"
        "M2qn3OJLTSesvMHP6UiIzdHWWKTR0PerTV7tGSCySlNXMGVlncX+PA8Rwr1FzPj"
        "wlw0Onuvy7pK4r1EyK6BD7ukadkjnggJ7vXF83SEzio02wzxpVo4pt3UPwzPvA9P"
        "aM+EMefaIDHC89Oa3R4/Jsgbd+1koYaC2HHi22eBzCwHOTHd3YexfKgzUr1uSO1n"
        "7F/jmazRjn3oWN8bWICqwM9C+nGe5RLXqwFAhV2PDPUKtsOvrQ0+yg5ZHk+zXldy"
        "3bfIpiXWcI/yr6TcYeYtKzHXRwzuqBWSw3FR+UL4GiKnyODr1LAh31E9MMTnddEF"
        "BwIDAQAB"
        "-----END PUBLIC KEY-----"
    }
    response = await async_client.post(
        "/users/me/public_key/",
        json=request_data,
        headers={"Authorization": f"Bearer {token.token}"},
    )
    assert response.status_code == 200
    keys_counts = await db_session.execute(select(func.count(UserKeys.id)))
    assert keys_counts.scalar_one() == 1
    assert response.json()["id"] is not None
    assert response.json()["public_key"] == request_data["public_key"]
