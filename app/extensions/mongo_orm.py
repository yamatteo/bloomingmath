from datetime import date
from enum import Enum
from os import getenv
from typing import List, Union, Set, Optional, Dict

from bson import ObjectId
from bson.codec_options import CodecOptions, TypeEncoder, TypeRegistry
from bson.errors import InvalidId
from dotenv import load_dotenv
from pydantic import BaseModel, Field, EmailStr
from pydantic import ValidationError
from pydantic.main import ModelMetaclass

from .mongo import mongo_engine, AsyncIOMotorCollection

load_dotenv()

MAX_FIND = int(getenv("MAX_FIND", 50))


def get_id(obj):
    """Try to return an ObjectId in every conceivable way, otherwise raise ValueError."""
    try:
        return ObjectId(obj)
    except (InvalidId, TypeError):
        try:
            return ObjectId(getattr(obj, "id"))
        except (InvalidId, TypeError, AttributeError):
            try:
                return ObjectId(obj["id"])
            except (InvalidId, TypeError, KeyError):
                try:
                    return ObjectId(obj["_id"])
                except (InvalidId, TypeError, KeyError):
                    raise ValueError(f"Can't find id in {obj!r}.")


def fix_object_id(obj, force=False):
    if force and isinstance(obj, (str, ObjectId)):
        try:
            return get_id(obj)
        except ValueError:
            return obj
    if force and isinstance(obj, list):
        return [ fix_object_id(item, force=True) for item in obj ]
    if isinstance(obj, dict):
        if "_id" in obj.keys():
            obj["_id"] = fix_object_id(obj["_id"], force=True)
        elif "id" in obj.keys():
            obj["_id"] = fix_object_id(obj["id"], force=True)
        if "id" in obj.keys():
            del obj["id"]
        for key, value in obj.items():
            if key != "id" and key != "_id":
                obj[key] = fix_object_id(value, force=force)
        return obj
    return obj


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return str(get_id(v))

    def to_object_id(self):
        return get_id(self)


class SetEncoder(TypeEncoder):
    python_type = set

    def transform_python(self, value):
        return list(value)


class DateEncoder(TypeEncoder):
    python_type = date

    def transform_python(self, value):
        return str(value)


orm_codec_options = CodecOptions(type_registry=TypeRegistry([
    SetEncoder(),
    DateEncoder(),
]))


class ObjectsProperty(ModelMetaclass):
    @property
    def collection(cls) -> AsyncIOMotorCollection:
        collection_name = getattr(cls, "__field_defaults__").get("collection_name")
        assert isinstance(collection_name, str)
        return mongo_engine.db.get_collection(collection_name, codec_options=orm_codec_options)


class Model(BaseModel, metaclass=ObjectsProperty):
    id: ObjectIdStr = Field(..., alias="_id")
    collection_name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda x: str(x),
        }
        orm_mode = True

    @classmethod
    async def find(cls, filter: dict) -> List["Model"]:
        filter = fix_object_id(filter)
        return [cls.parse_obj(item) for item in await cls.collection.find(filter).to_list(length=MAX_FIND)]

    @classmethod
    async def find_one(cls, filter: dict) -> Optional["Model"]:
        filter = fix_object_id(filter)
        try:
            return cls.parse_obj(await cls.collection.find_one(filter))
        except ValidationError:
            return None

    @classmethod
    async def find_one_and_set(cls, filter: dict, set: dict) -> None:
        filter = fix_object_id(filter)
        await cls.collection.find_one_and_update(
            filter=filter,
            update={"$set": set},
        )

    @classmethod
    async def find_one_and_push(cls, filter: dict, push: dict) -> None:
        filter = fix_object_id(filter)
        await cls.collection.find_one_and_update(
            filter=filter,
            update={"$push": push},
        )

    @classmethod
    async def find_one_and_add_to_set(cls, filter: dict, push: dict) -> None:
        filter = fix_object_id(filter)
        await cls.collection.find_one_and_update(
            filter=filter,
            update={"$addToSet": push},
        )

    @classmethod
    async def find_one_and_pull(cls, filter: dict, pull: dict) -> None:
        filter = fix_object_id(filter)
        await cls.collection.find_one_and_update(
            filter=filter,
            update={"$pull": pull},
        )

    @classmethod
    async def insert_one(cls, obj: dict) -> ObjectIdStr:
        return ObjectIdStr((await cls.collection.insert_one(obj)).inserted_id)

    @classmethod
    async def insert_many(cls, _list: list) -> List[ObjectIdStr]:
        __list = await cls.collection.insert_many([
            cls.validate_new_object(item) for item in _list
        ])
        return [ObjectIdStr(id) for id in __list.inserted_ids]

    @classmethod
    async def delete_one(cls, filter: dict) -> None:
        filter = fix_object_id(filter)
        await cls.collection.delete_one(filter)

    @classmethod
    def validate_new_object(cls, d) -> dict:
        d["_id"] = ObjectId()
        return cls.parse_obj(d).dict(exclude={"id"})

    def save(self) -> None:
        self.find_one_and_set(
            filter={"id": self.id},
            set=self.dict(exclude={"id"})
        )

__all__ = ["BaseModel", "Model", "Optional", "List", "Set", "EmailStr", "Union", "Enum", "Dict"]