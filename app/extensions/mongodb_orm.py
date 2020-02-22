from os import getenv
from typing import List, Union, Optional, Type
from typing import TypeVar

from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from fastapi import UploadFile
from pydantic import BaseModel, Field
from pydantic import ValidationError
from pydantic.main import ModelMetaclass

from .mongo import mongo_engine, AsyncIOMotorCollection

load_dotenv()

MAX_FIND = int(getenv("MAX_FIND", 50))


class ObjectIdStr(str):
    """A string that's a valid ObjectId."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return str(ObjectId(v))
        except (TypeError, InvalidId):
            raise ValidationError(f"Value {v!r} can't be converted into ObjectId")


class ObjectsProperty(ModelMetaclass):
    """Extends pydantic's ModelMetaclass to implement the `collection` property."""

    @property
    def collection(cls) -> AsyncIOMotorCollection:
        collection_name = getattr(cls, "__field_defaults__").get("collection_name")
        assert isinstance(collection_name, str)
        return mongo_engine.db.get_collection(collection_name)


def try_oid(value):
    """Return an ObjectId if the given value is a valid ObjectId, or the same value otherwise."""
    try:
        return ObjectId(value)
    except (TypeError, InvalidId):
        return value


def to_mongo(obj):
    """Prepare an object for interaction with mongo_engine collection."""
    if isinstance(obj, str):
        return try_oid(obj)
    elif isinstance(obj, list):
        return [to_mongo(item) for item in obj]
    elif isinstance(obj, dict):
        return {("_id" if key == "id" or key == "_id" else key): to_mongo(value) for key, value in obj.items()}
    elif isinstance(obj, Model):
        return to_mongo(obj.dict(by_alias=True, include={"id", "collection_name"}))
    else:
        return obj


def _export_(obj):
    """Recursive static method that implements Model.export method."""
    if isinstance(obj, (str, ObjectId)):
        return str(obj)
    elif isinstance(obj, list):
        return [_export_(item) for item in obj]
    elif isinstance(obj, dict):
        return {("id" if key == "id" or key == "_id" else key): _export_(value) for key, value in obj.items()}
    elif isinstance(obj, Model):
        return _export_(obj.dict())
    else:
        return obj


# TypeVar to represent the user-defined child class that will inherit from Model
T = TypeVar("T")


class Model(BaseModel, metaclass=ObjectsProperty):
    """Base class for model inheritance. Every model has an `id` and a `collection_name`."""
    id: ObjectIdStr = Field(..., alias="_id")
    collection_name: str = Field(...)

    # TODO add uniqueness constraints
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda x: str(x),
            ObjectIdStr: lambda x: str(x)
        }

    def dict(self, *args, **kwargs):
        kwargs.update({"by_alias": False})
        return super().dict(*args, **kwargs)

    @classmethod
    def new_obj(cls, obj: dict):
        """Parse objects when they have no id, setting a fake id."""
        if "id" in obj.keys() or "_id" in obj.keys():
            raise ValueError("Can't create a new object with a predetermined id.")
        obj["_id"] = "000000000000000000000000"
        return cls.parse_obj(obj)

    def export(self):
        """Returns a plain dict that is json encodable that can be sent as response."""
        return _export_(self)

    @classmethod
    async def insert_one(cls: Type[T], obj: dict) -> T:
        """Save the given object to database and return a model with the newly created id."""
        obj = to_mongo(cls.new_obj(obj).dict(exclude={"id"}))
        res = await cls.collection.insert_one(obj)
        obj["_id"] = res.inserted_id
        return cls.parse_obj(obj)

    @classmethod
    async def insert_many(cls: Type[T], _list: List[dict]) -> List[T]:
        """Save the given objects to database and return a list of models with their newly created ids."""
        res = await cls.collection.insert_many([
            to_mongo(cls.new_obj(item).dict(exclude={"id"})) for item in _list
        ])
        __list = [cls(id=new_id, **obj) for obj, new_id in zip(_list, res.inserted_id)]
        return __list

    @classmethod
    async def find(cls: Type[T], find: dict = None) -> List[T]:
        """Return a (possibly empty) list of models that match with the given `find`."""
        if find is None:
            find = {}
        else:
            find = to_mongo(find)
        return [cls.parse_obj(item) for item in await cls.collection.find(find).to_list(length=MAX_FIND)]

    @classmethod
    async def find_one(cls: Type[T], find: dict) -> Optional[T]:
        """Return a model that match with the given `find` or return None otherwise."""
        find = to_mongo(find)
        try:
            return cls.parse_obj(await cls.collection.find_one(find))
        except ValidationError:
            return None

    @classmethod
    async def find_one_and_set(cls: Type[T], find: dict, data: dict) -> T:
        """Update a model that match the given `find` with the specified `data` and returns the updated model."""
        find = to_mongo(find)
        data = to_mongo(data)
        return cls.parse_obj(await cls.collection.find_one_and_update(
            filter=find,
            update={"$set": data},
            return_document=True
        ))

    @classmethod
    async def find_one_and_push(cls: Type[T], find: dict, data: dict) -> T:
        """Push given `data` in a model that match the given `find` and returns the updated model."""
        find = to_mongo(find)
        data = to_mongo(data)
        return cls.parse_obj(await cls.collection.find_one_and_update(
            filter=find,
            update={"$push": data},
            return_document=True
        ))

    @classmethod
    async def find_one_and_add_to_set(cls: Type[T], find: dict, data: dict) -> T:
        """AddToSet given `data` in a model that match the given `find` and returns the updated model."""
        find = to_mongo(find)
        data = to_mongo(data)
        return cls.parse_obj(await cls.collection.find_one_and_update(
            filter=find,
            update={"$addToSet": data},
            return_document=True
        ))

    @classmethod
    async def find_one_and_pull(cls: Type[T], find: dict, data: dict) -> T:
        """Pull given `data` from a model that match the given `find` and returns the updated model."""
        find = to_mongo(find)
        data = to_mongo(data)
        return cls.parse_obj(await cls.collection.find_one_and_update(
            filter=find,
            update={"$pull": data},
            return_document=True
        ))

    @classmethod
    async def delete_one(cls, find: dict) -> None:
        """Delete a model that match with the given `find`."""
        find = to_mongo(find)
        await cls.collection.delete_one(find)

    def save(self: T) -> T:
        """Save the eventually modified model to database and return the model itself."""
        return self.find_one_and_set(
            find={"id": self.id},
            data=self.dict(exclude={"id"})
        )

    @classmethod
    def ref(cls, obj_id) -> dict:
        """Returns a reference to an object in the calling collection with the given id (no existence check)."""
        return {
            "id": str(obj_id),
            "collection_name": getattr(cls, "__field_defaults__").get("collection_name")
        }

    def self_ref(self) -> dict:
        """Returns a reference to self (no existence check)."""
        return {
            "id": str(self.id),
            "collection_name": self.collection_name
        }


class FileModel(BaseModel, metaclass=ObjectsProperty):
    """Base class for model inheritance of file bearing model. Every model has an `id` and a `collection_name`."""
    id: ObjectIdStr = Field("000000000000000000000000", alias="_id")
    original_filename: str = Field("")
    collection_name: str = Field(...)

    # TODO add uniqueness constraints
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda x: str(x),
            ObjectIdStr: lambda x: str(x)
        }

    @classmethod
    async def insert_one(cls: Type[T], content: UploadFile, data: dict) -> T:
        grid_in, file_id = mongo_engine.fs.open_upload_stream(
            content.filename,
            metadata=to_mongo(cls.parse_obj(data))
        )
        with content.file as f:
            await grid_in.write(f.read())
            await grid_in.set("_id", file_id)
            await grid_in.set("original_filename", content.filename)
            await grid_in.close()
        data["_id"] = file_id
        return cls.parse_obj(data)

    @classmethod
    async def find(cls: Type[T], find: dict = {}) -> List[T]:
        find = to_mongo(find)
        cursor = mongo_engine.fs.find({"metadata": find}, no_cursor_timeout=True)
        return [cls.parse_obj(grid_data.metadata) for grid_data in cursor]

    @classmethod
    async def find_one(cls: Type[T], find: dict) -> Optional[T]:
        find = to_mongo(find)
        cursor = mongo_engine.fs.find({"metadata": find}, no_cursor_timeout=True)
        finds = [cls.parse_obj(grid_data.metadata) for grid_data in cursor]
        try:
            return finds.pop()
        except IndexError:
            return None

    @classmethod
    async def find_one_and_set(cls: Type[T], find: dict, data: dict) -> Optional[T]:
        find = to_mongo(find)
        data = to_mongo(data)
        cursor = mongo_engine.fs.find({"metadata": find}, no_cursor_timeout=True)
        finds = [cls.parse_obj(grid_data.metadata) for grid_data in cursor]
        try:
            obj = finds.pop()
        except IndexError:
            return None
        grid_in, _ = mongo_engine.fs.open_upload_stream_with_id(file_id=obj.id, filename=obj.original_filename)
        for key, value in data.items():
            await grid_in.set(key, value)
        await grid_in.close()
        dobj = obj.dict()
        dobj.update(data)
        return cls.parse_obj(dobj)

    @classmethod
    async def delete(cls: Type[T], find: dict) -> None:
        find = to_mongo(find)
        cursor = mongo_engine.fs.find({"metadata": find}, no_cursor_timeout=True)
        finds = [cls.parse_obj(grid_data.metadata) for grid_data in cursor]
        for obj in finds:
            await mongo_engine.fs.delete(ObjectId(obj.id))



One = Union[T, Model]
Many = List[One]
Maybe = Union[T, None]
