import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.config import settings
from app.crud.crud_user import create_user, create_user_token
from app.db.base import Base, User, UserToken, UserGroup
from app.main import app
from app.schemas.user import UserCreate
from app.schemas.user_group import UserGroupBase
from app.crud.crud_user_group import create_user_group


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(settings.TEST_SQLALCHEMY_DATABASE_URL)
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def prepare_db():
    create_db_engine = create_async_engine(
        settings.POSTGRES_DATABASE_URL,
        isolation_level="AUTOCOMMIT",
    )
    async with create_db_engine.begin() as connection:
        await connection.execute(
            text(
                "drop database if exists {name};".format(
                    name=settings.TEST_DB_NAME
                )
            ),
        )
        await connection.execute(
            text("create database {name};".format(name=settings.TEST_DB_NAME)),
        )


@pytest_asyncio.fixture(scope="session")
async def db_session(engine) -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        TestingSessionLocal = sessionmaker(
            expire_on_commit=False,
            class_=AsyncSession,
            bind=engine,
        )
        async with TestingSessionLocal(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture(scope="session")
def override_get_db(prepare_db, db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest_asyncio.fixture(scope="session")
async def async_client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def user(db_session: AsyncSession) -> User:
    user = UserCreate(email="test@test.com", name="Hello", password="12345678")
    user_db = await create_user(db_session, user)
    yield user_db
    await db_session.delete(user_db)
    await db_session.commit()


@pytest_asyncio.fixture
async def user_group(db_session: AsyncSession, user: User) -> UserGroup:
    user_group = UserGroupBase(name="Hello")
    user_group_db = await create_user_group(db_session, user, user_group)
    yield user_group_db
    await db_session.delete(user_group_db)
    await db_session.commit()


@pytest_asyncio.fixture
async def token(db_session: AsyncSession, user: User) -> UserToken:
    token_db = await create_user_token(db_session, user)
    return token_db
