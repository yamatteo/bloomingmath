from collections import namedtuple
from multiprocessing import Process

from bson import ObjectId
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorDatabase
from pytest import fixture
from pytest import mark, yield_fixture
from pytest import raises
from starlette.testclient import TestClient  # If problems arises with testing middleware, prefer async_asgi_testclient
from uvicorn import run as uvicorn_run

from .mongo import AlreadyInitializedError
from .mongo import mongo_engine
from .mongo import NotInitializedError
from .mongo_orm import Model, ObjectIdStr, List, Union, Set

import asyncio


@yield_fixture(scope="module")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture(scope="module")
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


@fixture(scope="module")
async def setup(check_local_mongodb):
    """Returns an AsyncIOMotorEngine, a FastAPI application and a Starlette TestClient."""
    me = mongo_engine
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


class Item(Model):
    collection_name: str = "items"
    foo: int
    bar: str


class Drawer(Model):
    collection_name: str = "drawers"
    color: str
    items: Set[Union["Item", ObjectIdStr]]


class Closet(Model):
    collection_name: str = "closets"
    name: str
    drawers: List[Union["Drawer", ObjectIdStr]]

    def some_function(self):
        return 34


@mark.asyncio
async def test_models_creation(setup):
    me, app, client = setup
    ids = await Item.insert_many([
        {"foo": 1, "bar": "baz"},
        {"foo": 2, "bar": "bar"},
        {"foo": 3, "bar": "baz"},
        {"foo": 4, "bar": "baz"},
        {"foo": 5, "bar": "bar"},
        {"foo": 6, "bar": "bar"},
    ])
    drawers_ids = await Drawer.insert_many([
        {"color": "white", "items": ids[0:2]},
        {"color": "black", "items": ids[2:4]},
        {"color": "red", "items": {ids[5]}},
    ])
    id = await Closet.insert_one({"name": "kitchen closet", "drawers": drawers_ids})
    assert {'collection_name': 'closets',
            'drawers': drawers_ids,
            'id': id,
            'name': 'kitchen closet'} == (await Closet.find_one({})).dict()
