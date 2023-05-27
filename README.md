# FastAPI with async SQLAlchemy, alembc, celery and wecbsockets
Starting from version 1.4 [SQLAlchemy supports asyncio](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html).
This means you don't need externla tools like [encode/databases](https://github.com/encode/databases).
This educational project demonstrates how you can use new [SQLAlchemy 2.0-style](https://docs.sqlalchemy.org/en/14/glossary.html#term-1) with FastAPI.
Websockets, celery and alembic for DB migrations are used as well.

If you are interesting in old styled SQLAlchemy async example you can check [this repo](https://github.com/NeverWalkAloner/async-blogs).

## Build
Run
```
$ docker compose up --build
```

## Tests
Tu run tests use
```
$ docker compose exec web pytest
```

## Documentation
To open API documentation go here: http://127.0.0.1:8000/docs

## Websockets
If you want to test websocket, you can run simple and websocket client:
```
python websocket_test_client/main.py <USER_TOKEN>
```
Please note that you need user token for this. You can create user like this:
```
curl --location 'http://0.0.0.0:8000/sign-up/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "hello@world.com",
    "password": "12345678",
    "name": "Sam Vimes"
}'
