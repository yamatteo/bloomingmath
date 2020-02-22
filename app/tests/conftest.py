from asyncio import get_event_loop_policy
from collections import namedtuple
from logging import warning

import nest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pytest import fixture
from pytest import yield_fixture
from starlette.testclient import TestClient  # If problems arises with testing middleware, prefer async_asgi_testclient

# from uvicorn import run as uvicorn_run
from extensions.mongo import mongo_engine
from extensions.mongo import mongo_engine as me
from extensions.security import create_access_token
from extensions.security import get_password_hash
from main import app


# from multiprocessing import Process


# This is not sure: pytest-asyncio run coroutine test and so needs an event_loop.
# If I want a package scoped fixture I need to provide a package scoped event_loop.
@yield_fixture(scope="package")
def event_loop(request):
    loop = get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Sometimes test fails and it take a long time to figure out that simply mongod is not running locally.
# This fixture provides immediately that useful information.
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
    me = mongo_engine
    # # This was an old way of running the server. Looks like TestClient is enough.
    # process = Process(target=uvicorn_run,
    #                   args=(app,),
    #                   kwargs={
    #                       "host": "127.0.0.1",
    #                       "port": 8070,
    #                       "log_level": "info"},
    #                   daemon=True)
    # process.start()

    # In normal use, it is unicorn that calls the startup handlers
    for handler in app.router.lifespan.startup_handlers:
        await handler()

    # This is not sure: I'm using pytest-asyncio and it start a loop;
    # inside of that loop I start a TestClient which needs a loop for itself; that is why I need to apply nest_asyncio.
    nest_asyncio.apply()

    client = TestClient(app=app, base_url="http://127.0.0.1:8080")

    # At each test the database is dropped. Need to make some objects to speedup tests.
    admin_token, user_token = await populate()

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

    # If the process is forken in the setpu it should terminate in the teardown.
    # process.terminate()


async def populate():
    from models import User, Content, Node, Group
    warning(f"Setting a fresh development database.")
    await me.db.drop_collection("users")
    await me.db.drop_collection("groups")
    await me.db.drop_collection("nodes")
    await me.db.drop_collection("contents")
    user_id = (await me.collection("users").insert_one({
        "email": "user@example.com",
        "password_hash": get_password_hash("pass"),
    })).inserted_id
    admin_id = (await me.collection("users").insert_one({
        "email": "admin@example.com",
        "password_hash": get_password_hash("pass"),
        "is_admin": True,
    })).inserted_id

    node_id = (await me.collection("nodes").insert_one({
        "short": "Argument 10",
        "long": "# Description of argument 10 \n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "contents": []
    })).inserted_id

    await me.collection("groups").insert_one({
        "short": "First",
        "long": "Description of the first group",
        "members": [{
            "_id": user_id,
            "collection_name": "users"
        }, {
            "_id": admin_id,
            "collection_name": "users"
        }],
        "nodes": [{
            "_id": node_id,
            "collection_name": "nodes"
        }]
    })

    user_token = create_access_token(
        data={"sub": str(user_id)}
    )
    admin_token = create_access_token(
        data={"sub": str(admin_id)}
    )
    return admin_token, user_token
