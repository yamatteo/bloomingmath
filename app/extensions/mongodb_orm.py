from os import getenv
from typing import AnyStr
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
from typing import ByteString

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


def to_mongo(obj, only_ref=False, exclude_id=False):
    """Prepare an object for interaction with mongo_engine collection."""
    if isinstance(obj, str):
        return try_oid(obj)
    elif isinstance(obj, list):
        return [to_mongo(item, only_ref=only_ref, exclude_id=exclude_id) for item in obj]
    elif isinstance(obj, dict):
        if exclude_id:
            return {key: to_mongo(value, only_ref=only_ref, exclude_id=exclude_id) for key, value in obj.items() if
                    key != "id" and key != "_id"}
        else:
            return {("_id" if key == "id" or key == "_id" else key): to_mongo(value, only_ref=only_ref,
                                                                              exclude_id=exclude_id) for key, value in
                    obj.items()}
    elif isinstance(obj, (Model, ModelWithContentFile)):
        if only_ref:
            return to_mongo(obj.dict(by_alias=True, include={"id", "collection_name"}), only_ref=True, exclude_id=False)
        else:
            return to_mongo(dict(obj), only_ref=True, exclude_id=exclude_id)
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
    async def insert_one(cls: Type[T], data: dict) -> T:
        """Save the given object to database and return a model with the newly created id."""
        data = to_mongo(cls.new_obj(data), exclude_id=True)
        res = await cls.collection.insert_one(data)
        data["_id"] = res.inserted_id
        return cls.parse_obj(data)

    @classmethod
    async def insert_many(cls: Type[T], _list: List[dict]) -> List[T]:
        """Save the given objects to database and return a list of models with their newly created ids."""
        res = await cls.collection.insert_many([
            to_mongo(cls.new_obj(item), exclude_id=True) for item in _list
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

    async def save(self: T) -> T:
        """Save the eventually modified model to database and return the model itself."""
        return await self.find_one_and_set(
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


# class FileModel(BaseModel, metaclass=ObjectsProperty):
#     """Base class for model inheritance of file bearing model. Every model has an `id` and a `collection_name`."""
#     id: ObjectIdStr = Field("000000000000000000000000", alias="_id")
#     original_filename: str = Field("")
#     collection_name: str = Field(...)
#
#     # TODO add uniqueness constraints
#     class Config:
#         allow_population_by_field_name = True
#         json_encoders = {
#             ObjectId: lambda x: str(x),
#             ObjectIdStr: lambda x: str(x)
#         }
#
#     @classmethod
#     async def _find_many(cls: Type[T], find: dict = {}) -> List[dict]:
#         find = {f"metadata.{key}": value for key, value in to_mongo(find).items()}
#         return await mongo_engine.db.get_collection("fs.files").find(find).to_list(length=MAX_FIND)
#
#     @classmethod
#     async def _find_one(cls: Type[T], find: dict = {}) -> Optional[dict]:
#         find = {f"metadata.{key}": value for key, value in to_mongo(find).items()}
#         return await mongo_engine.db.get_collection("fs.files").find_one(find)
#
#     def dict(self, *args, **kwargs):
#         kwargs.update({"by_alias": False})
#         return super().dict(*args, **kwargs)
#
#     @classmethod
#     async def insert_one(cls: Type[T], content: UploadFile, data: dict) -> T:
#         file_id = ObjectId()
#         data["_id"] = file_id
#         data["original_filename"] = content.filename
#         grid_in = mongo_engine.fs.open_upload_stream_with_id(
#             file_id=file_id,
#             filename=content.filename,
#             metadata=to_mongo(cls.parse_obj(data))
#         )
#         with content.file as f:
#             await grid_in.write(f.read())
#             await grid_in.close()
#         return cls.parse_obj(data)
#
#     @classmethod
#     async def find(cls: Type[T], find: dict = {}) -> List[T]:
#         grid_objs = await cls._find_many(find)
#         return [cls.parse_obj(grid_obj["metadata"]) for grid_obj in grid_objs]
#
#     @classmethod
#     async def find_one(cls: Type[T], find: dict) -> Optional[T]:
#         try:
#             grid_obj = await cls._find_one(find)
#             return cls.parse_obj(grid_obj["metadata"])
#         except (AttributeError, TypeError, ValidationError):
#             return None
#
#     @classmethod
#     async def find_one_and_set(cls: Type[T], find: dict, data: dict) -> Optional[T]:
#         data = to_mongo(data)
#         grid_obj = await cls._find_one(find)
#         obj = cls.parse_obj(grid_obj["metadata"])
#         fs_files = await mongo_engine.db.get_collection("fs.files").find_one_and_update(
#             filter={"_id": ObjectId(obj.id)},
#             update={"$set": {f"metadata.{field_name}": field_value for field_name, field_value in data.items()}},
#             return_document=True
#         )
#         dobj = obj.dict()
#         dobj.update(data)
#         return cls.parse_obj(dobj)
#
#     @classmethod
#     async def find_one_and_upload(cls: Type[T], find: dict, data: UploadFile) -> Optional[T]:
#         try:
#             grid_obj = await cls._find_one(find)
#             obj = cls.parse_obj(grid_obj["metadata"])
#             file_id = ObjectId()
#             grid_in = mongo_engine.fs.open_upload_stream_with_id(
#                 file_id=file_id,
#                 filename=obj.original_filename,
#                 metadata=to_mongo(obj)
#             )
#             with data.file as f:
#                 await grid_in.write(f.read())
#                 await grid_in.close()
#             return obj
#         except (AttributeError, TypeError, ValidationError):
#             return None
#
#
#     @classmethod
#     async def delete(cls: Type[T], find: dict) -> None:
#         grid_objs = await cls._find_many(find)
#         objs = [cls.parse_obj(grid_obj["metadata"]) for grid_obj in grid_objs]
#         for obj in objs:
#             await mongo_engine.fs.delete(ObjectId(obj.id))
#
#     @classmethod
#     async def read(cls: Type[T], id: str) -> bytes:
#         meta_content = await mongo_engine.db.get_collection("fs.files").find_one({"metadata._id": ObjectId(id)})
#         print(id)
#         print(meta_content)
#         from tempfile import TemporaryFile
#         with TemporaryFile() as file:
#             await mongo_engine.fs.download_to_stream(meta_content["_id"], file)
#             file.seek(0)
#             data = file.read()
#         return data

class ModelWithContentFile(Model):
    related_content_id: Optional[ObjectIdStr] = None

    async def upload(self: T, data: UploadFile) -> T:
        rcid = await mongo_engine.fs.upload_from_stream(
            filename=data.filename,
            source=data.file,
        )
        if self.related_content_id is not None:
            await mongo_engine.fs.delete(ObjectId(self.related_content_id))
        self.related_content_id = rcid
        self.original_filename = data.filename

        return await self.save()

    async def download(self) -> bytes:
        from tempfile import TemporaryFile
        if self.related_content_id is None:
            raise Exception("No related content.")
        with TemporaryFile() as file:
            await mongo_engine.fs.download_to_stream(ObjectId(self.related_content_id), file)
            file.seek(0)
            return file.read()


One = Union[T, Model]
Many = List[One]
Maybe = Union[T, None]
