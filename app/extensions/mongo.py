from logging import info
from typing import Optional

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorDatabase
from motor.motor_asyncio import AsyncIOMotorGridFSBucket


class NotInitializedError(RuntimeError):
    pass


class AlreadyInitializedError(RuntimeError):
    pass


class AsyncIOMotorEngine:
    """Object that binds together AsyncIOMotorClient, AsyncIOMotorDatabase and AsyncIOMotorGridFSBucket.

    The engine is created at once and later initialized with the app (by :func: init_app) to make sure there is only
    one instance and one open connection to the database."""
    app_string: Optional[str] = None
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    fs: Optional[AsyncIOMotorGridFSBucket] = None
    environment: Optional[str] = None

    def collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """Return the requested :class: `AsyncIOMotorCollection`.

        :param collection_name: Name of the collection to get
        :type collection_name: str

        :raises NotInitializedError: Cannot get collections when the engine was not initialized

        :return: The requested collection
        :rtype: AsyncIOMotorCollection
        """
        if any(obj is None for obj in (self.app_string, self.client, self.db, self.fs, self.environment)):
            raise NotInitializedError("Engine is not initialized.")
        return self.db.get_collection(collection_name)

    def init_app(self, app: FastAPI, uri: Optional[str] = None, db_name: Optional[str] = None,
                 env: str = "development") -> None:
        """Define self.app_string and add 'startup' and 'shutdown' event handlers to the given FastAPI application.

        :param app: The relevant FastAPI application
        :type app: class: FastAPI
        :param uri: Where to find the database; defaults to None, in which case localhost:27027 will be used
        :type uri: str, optional
        :param db_name: Name of the database to use; if None, a name will be generated based on the title of the FastAPI app provided to the init_app method
        :type db_name: str, optional
        :param env: The environment in which the app is running, defaults to 'development'
        :type env: str

        :raises AlreadyInitializedError: Cannot init an app that has already been initialized
        """

        async def connect():
            await self.connect_to_mongo(uri=uri, db_name=db_name)

        async def close():
            await self.close_mongo_connection()

        if any(obj is not None for obj in (self.app_string, self.client, self.db, self.fs, self.environment)):
            raise AlreadyInitializedError("Engine is already initialized.")
        self.app_string = ''.join(c if c.isalpha() else "_" for c in list(app.title.lower()))
        self.environment = env
        app.add_event_handler("startup", connect)
        app.add_event_handler("shutdown", close)

    async def connect_to_mongo(self, uri=None, db_name=None) -> None:
        """Open an asynchronous connection to a mongo database.

        :param uri: Where to find the database; defaults to None, in which case localhost:27027 will be used
        :type uri: str, optional
        :param db_name: Name of the database to use; if None, a name will be generated based on the title of the FastAPI app provided to the init_app method
        :type db_name: str, optional
        """
        info("Connecting to the database...")
        if uri:
            self.client = AsyncIOMotorClient(uri)
        else:
            self.client = AsyncIOMotorClient()
        if db_name:
            self.db = self.client[db_name]
        else:
            self.db = self.client[f"{self.app_string}_{self.environment}"]
        self.fs = AsyncIOMotorGridFSBucket(self.db)
        info(f"Database {db_name} connection succeeded！")

    async def close_mongo_connection(self):
        """Close the client."""
        self.client.close()
        info("Database connection closed！")


mongo_engine = AsyncIOMotorEngine()

__all__ = ("mongo_engine", "NotInitializedError", "AlreadyInitializedError")
