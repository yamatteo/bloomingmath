from collections import namedtuple
from multiprocessing import Process

from bson import ObjectId
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorDatabase
from pytest import fixture
from pytest import mark
from pytest import raises
from starlette.testclient import TestClient  # If problems arises with testing middleware, prefer async_asgi_testclient
from uvicorn import run as uvicorn_run

from .mongo import AlreadyInitializedError
from .mongo import AsyncIOMotorEngine
from .mongo import NotInitializedError


@fixture(autouse=True)
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


@fixture
async def setup(check_local_mongodb):
    """Returns an AsyncIOMotorEngine, a FastAPI application and a Starlette TestClient."""
    me = AsyncIOMotorEngine()
    app = FastAPI()
    me.init_app(app)
    process = Process(target=uvicorn_run,
                      args=(app,),
                      kwargs={
                          "host": "127.0.0.1",
                          "port": 8080,
                          "log_level": "info"},
                      daemon=True)
    process.start()

    # In normal use, it is unicorn that calls the startup handlers
    for handler in app.router.lifespan.startup_handlers:
        await handler()

    client = TestClient(app=app, base_url="http://127.0.0.1:8080")
    yield namedtuple("SETUP_TUPLE", "me app client")(me, app, client)

    # In normal use, it is unicorn that calls the shutdown handlers
    for handler in app.router.lifespan.shutdown_handlers:
        await handler()

    await me.client.drop_database(me.db)
    process.terminate()


@mark.asyncio
async def test_initialization(setup):
    """Test if AsyncIOMotorEngine and FastAPI are properly initialized."""
    me, app, client = setup

    assert me.environment == "development"
    assert me.app_string == "fastapi"

    assert isinstance(me.client, AsyncIOMotorClient)
    assert isinstance(me.db, AsyncIOMotorDatabase)
    assert isinstance(me.collection("collection"), AsyncIOMotorCollection)

    other_me = AsyncIOMotorEngine()
    with raises(NotInitializedError):
        assert isinstance(other_me.collection("collection"), AsyncIOMotorCollection)

    other_app = FastAPI(title="Other app")
    with raises(AlreadyInitializedError):
        me.init_app(other_app)

    other_me.init_app(other_app, uri="mongodb://1.2.3.4:27017", db_name="database_name", env="production")

    assert other_me.environment == "production"
    assert other_me.app_string == "other_app"


@mark.asyncio
async def test_database_interaction(setup):
    """Test common interaction with a mongo database."""
    me, app, client = setup
    await me.collection("items").drop()
    assert 0 == await me.collection("items").count_documents({})
    await me.collection("items").insert_one({"foo": "bar"})
    item = await me.collection("items").find_one({"foo": "bar"})
    assert isinstance(item, dict)
    assert item["foo"] == "bar"
    assert isinstance(item["_id"], ObjectId)
    item = await me.collection("items").find_one({"foo": "baz"})
    assert item is None
    await me.collection("items").find_one_and_update(filter={"foo": "bar"}, update={"$set": {"foo": "baz"}})
    item = await me.collection("items").find_one({"foo": "baz"})
    assert item["foo"] == "baz"
    await me.collection("items").find_one_and_replace(filter={"foo": "baz"}, replacement={"bar": "baz"})
    item = await me.collection("items").find_one({"bar": "baz"})
    assert item["bar"] == "baz"
    await me.collection("items").find_one_and_delete({"bar": "baz"})
    assert 0 == await me.collection("items").count_documents({})

    await me.collection("items").insert_many([
        {"foo": 1},
        {"foo": 2},
        {"foo": 1, "baz": 3}
    ])
    assert 3 == await me.collection("items").count_documents({})
    find_list = await me.collection("items").find({"foo": 1}).to_list(length=50)
    assert isinstance(find_list, list)
    assert len(find_list) == 2
    find_list = await me.collection("items").find({"foo": 4}).to_list(length=50)
    assert len(find_list) == 0
