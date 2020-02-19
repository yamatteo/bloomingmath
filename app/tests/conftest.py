from asyncio import get_event_loop_policy
from collections import namedtuple
from multiprocessing import Process

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pytest import fixture
from pytest import yield_fixture
from starlette.testclient import TestClient  # If problems arises with testing middleware, prefer async_asgi_testclient
from uvicorn import run as uvicorn_run

from extensions.mongo import mongo_engine


@yield_fixture(scope="package")
def event_loop(request):
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture(scope="package", autouse=True)
async def check_local_mongodb():
    """Assure that a local mongodb server is running."""
    import pymongo.errors
    client = AsyncIOMotorClient(serverSelectionTimeoutMS=2000)
    try:
        await client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError:
        raise pymongo.errors.ServerSelectionTimeoutError(
            "A local mongodb server is needed for testing and does not seem to be running."
        )


@fixture(scope="package")
async def setup():
    """Returns an AsyncIOMotorEngine, a FastAPI application and a Starlette TestClient."""
    from extensions.mongo import mongo_engine
    from main import app

    me = mongo_engine
    process = Process(target=uvicorn_run,
                      args=(app,),
                      kwargs={
                          "host": "127.0.0.1",
                          "port": 8070,
                          "log_level": "info"},
                      daemon=True)
    process.start()

    import nest_asyncio
    nest_asyncio.apply()

    # In normal use, it is unicorn that calls the startup handlers
    for handler in app.router.lifespan.startup_handlers:
        await handler()

    client = TestClient(app=app, base_url="http://127.0.0.1:8070")

    # TODO setup usual user and admin
    from extensions.security import get_password_hash
    user_id = (await me.collection("users").insert_one({
        "email": "user@example.com",
        "password_hash": get_password_hash("pass"),
    })).inserted_id
    admin_id = (await me.collection("users").insert_one({
        "email": "admin@example.com",
        "password_hash": get_password_hash("pass"),
        "is_admin": True,
    })).inserted_id

    from extensions.security import create_access_token
    user_token = create_access_token(
        data={"sub": str(user_id)}
    )
    admin_token = create_access_token(
        data={"sub": str(admin_id)}
    )

    def admin_login():
        client.headers.update({"Authorization": f"Bearer {admin_token.decode('utf-8')}"})
    def user_login():
        client.headers.update({"Authorization": f"Bearer {user_token.decode('utf-8')}"})
    def logout():
        client.headers.update({"Authorization": "Bearer"})

    yield namedtuple("SETUP_TUPLE", "me app client alog ulog logout")(me, app, client, admin_login, user_login, logout)

    # In normal use, it is unicorn that calls the shutdown handlers
    for handler in app.router.lifespan.shutdown_handlers:
        await handler()

    await me.client.drop_database(me.db)
    process.terminate()
