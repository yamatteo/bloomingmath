from os import getenv
from typing import List, Union, Optional, Type
from typing import TypeVar

from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
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


class TemporaryObjectIdStr(ObjectIdStr):
    """A string to parse new objects when they still have no id."""

    @classmethod
    def validate(cls, v):
        return ""


# def bson(obj, force=False):
#     if force:
#         if isinstance(obj, str):
#             try:
#                 return ObjectId(obj)
#             except:
#                 return obj
#         elif isinstance(obj, list):
#             return [bson(item, force=True) for item in obj]
#         elif isinstance(obj, dict):
#             _obj = {key: bson(value, force=True) for key, value in obj.items()}
#             if "id" in _obj.keys():
#                 _obj["_id"] = _obj["id"]
#                 del _obj["id"]
#             return _obj
#         else:
#             return obj
#     elif isinstance(obj, dict):
#         obj = { key: bson(value) for key, value in obj.items()}
#         if "id" in obj.keys():
#             obj["_id"] = bson(obj["id"], force=True)
#             del obj["id"]
#         return obj
#     else:
#         return obj


# class SetEncoder(TypeEncoder):
#     python_type = set
#
#     def transform_python(self, value):
#         return list(value)
#
#
# class DateEncoder(TypeEncoder):
#     python_type = date
#
#     def transform_python(self, value):
#         return str(value)
#
#
# orm_codec_options = CodecOptions(type_registry=TypeRegistry([
#     SetEncoder(),
#     DateEncoder(),
# ]))


class ObjectsProperty(ModelMetaclass):
    @property
    def collection(cls) -> AsyncIOMotorCollection:
        collection_name = getattr(cls, "__field_defaults__").get("collection_name")
        assert isinstance(collection_name, str)
        return mongo_engine.db.get_collection(collection_name)
        # return mongo_engine.db.get_collection(collection_name, codec_options=orm_codec_options)


def try_oid(value):
    try:
        return ObjectId(value)
    except (TypeError, InvalidId):
        return value


def bson(obj):
    if isinstance(obj, str):
        return try_oid(obj)
    elif isinstance(obj, list):
        return [bson(item) for item in obj]
    elif isinstance(obj, dict):
        return {("_id" if key == "id" or key == "_id" else key): bson(value) for key, value in obj.items()}
    elif isinstance(obj, BareModel):
        return bson(obj.dict(by_alias=True, include={"id", "collection_name"}))
    else:
        return obj


def _export_(obj):
    if isinstance(obj, (str, ObjectId)):
        return str(obj)
    elif isinstance(obj, list):
        return [_export_(item) for item in obj]
    elif isinstance(obj, dict):
        return {("id" if key == "id" or key == "_id" else key): _export_(value) for key, value in obj.items()}
    elif isinstance(obj, BareModel):
        return _export_(obj.dict())
    else:
        return obj


T = TypeVar("T")


class BareModel(BaseModel, metaclass=ObjectsProperty):
    id: ObjectIdStr = Field(TemporaryObjectIdStr(), alias="_id")
    collection_name: str = Field(...)

    class Config:
        allow_population_by_field_name = True

    # def __repr__(self):
    #     c = self.collection_name.capitalize()
    #     i = str(self.id)
    #     return f"{c}#{i}"

    def export(self):
        return _export_(self)

    @classmethod
    async def insert_one(cls, obj: dict) -> ObjectId:
        obj = bson(obj)
        return ObjectId((await cls.collection.insert_one(obj)).inserted_id)

    @classmethod
    async def insert_many(cls, _list: List[dict]) -> List[ObjectId]:
        __list = await cls.collection.insert_many([
            bson(cls.parse_obj(item).dict(exclude={"id"})) for item in _list
            # bson(cls.validate_new_object(item)) for item in _list
        ])
        return [ObjectId(_id) for _id in __list.inserted_ids]

    @classmethod
    async def find(cls: Type[T], find: dict = None) -> List[T]:
        if find is None:
            find = {}
        else:
            find = bson(find)
        return [cls.parse_obj(item) for item in await cls.collection.find(find).to_list(length=MAX_FIND)]

    @classmethod
    async def find_one(cls: Type[T], find: dict) -> Optional[T]:
        find = bson(find)
        try:
            return cls.parse_obj(await cls.collection.find_one(find))
        except ValidationError:
            return None

    @classmethod
    async def find_one_and_set(cls: Type[T], find: dict, data: dict) -> Optional[T]:
        find = bson(find)
        data = bson(data)
        return cls.parse_obj(await cls.collection.find_one_and_update(
            filter=find,
            update={"$set": data},
            return_document=True
        ))

    @classmethod
    async def find_one_and_push(cls: Type[T], find: dict, data: dict) -> Optional[T]:
        find = bson(find)
        data = bson(data)
        return cls.parse_obj(await cls.collection.find_one_and_update(
            filter=find,
            update={"$push": data},
            return_document=True
        ))

    @classmethod
    async def find_one_and_add_to_set(cls: Type[T], find: dict, data: dict) -> Optional[T]:
        find = bson(find)
        data = bson(data)
        return cls.parse_obj(await cls.collection.find_one_and_update(
            filter=find,
            update={"$addToSet": data},
            return_document=True
        ))

    @classmethod
    async def find_one_and_pull(cls: Type[T], find: dict, data: dict) -> Optional[T]:
        find = bson(find)
        data = bson(data)
        return cls.parse_obj(await cls.collection.find_one_and_update(
            filter=find,
            update={"$pull": data},
            return_document=True
        ))

    @classmethod
    async def delete_one(cls, find: dict) -> None:
        find = bson(find)
        await cls.collection.delete_one(find)

    # @classmethod
    # def validate_new_object(cls, obj) -> dict:
    #     obj = bson(obj)
    #     if "_id" not in obj.keys():
    #         obj["_id"] = ObjectId()
    #     return cls.parse_obj(obj).dict(exclude={"id"})

    def save(self) -> None:
        self.find_one_and_set(
            find={"id": self.id},
            data=bson(self.dict(exclude={"id"}))
        )

    @classmethod
    def ref(cls, obj_id) -> dict:
        return {
            "id": str(obj_id),
            "collection_name": getattr(cls, "__field_defaults__").get("collection_name")
        }

    def self_ref(self) -> dict:
        return {
            "id": str(self.id),
            "collection_name": self.collection_name
        }


One = Union[T, BareModel]
Many = List[One]
Maybe = Union[T, None]
