from typing import Optional, List, Union, Any

from pydantic import BaseModel, EmailStr, validator, root_validator
from models import User, Content, Node, Group, ExternalContent, Model


class UserSignup(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str

    @validator("password")
    def password_is_not_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Password can't be an empty string.")
        return value

    @root_validator
    def passwords_match(cls, values):
        pw1, pw2 = values.get("password"), values.get("password_confirmation")
        if pw1 != pw2:
            raise ValueError(f"Passwords do not match ({pw1} vs. {pw2}).")
        return values

class UserPasswordReset(BaseModel):
    email: EmailStr
    token: str
    password: str
    password_confirmation: str

    @validator("password")
    def password_is_not_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Password can't be an empty string.")
        return value

    @root_validator
    def passwords_match(cls, values):
        pw1, pw2 = values.get("password"), values.get("password_confirmation")
        if pw1 != pw2:
            raise ValueError(f"Passwords do not match ({pw1} vs. {pw2}).")
        return values

class UserForgotPassword(BaseModel):
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_is_not_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Password can't be an empty string.")
        return value

class UserFind(BaseModel):
    id: Optional[Any]
    email: Optional[Any]

class UserFindOne(BaseModel):
    id: Optional[str]
    email: Optional[str]


class UserAdd(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False
    is_blocked: bool = False


class UserEdit(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]
    is_blocked: Optional[bool]

class ContentFind(BaseModel):
    id: Optional[str]
    short: Optional[str]
    filetype: Optional[str]
    original_filename: Optional[str]

class ContentAdd(BaseModel):
    short: str
    long: Optional[str]
    filetype: str

class ContentEdit(BaseModel):
    short: Optional[str]
    long: Optional[str]
    filetype: Optional[str]


class ExternalContentFind(BaseModel):
    id: Optional[str]
    short: Optional[str]
    url: Optional[str]

class ExternalContentAdd(BaseModel):
    short: str
    long: Optional[str]
    url: str

class ExternalContentEdit(BaseModel):
    short: Optional[str]
    long: Optional[str]
    url: Optional[str]


class GroupFind(BaseModel):
    id: Optional[str]
    short: Optional[str]
    long: Optional[str]

class GroupAdd(BaseModel):
    short: str
    long: Optional[str]

class GroupEdit(BaseModel):
    short: Optional[str]
    long: Optional[str]
    nodes: Optional[List[Union[Node, Model]]]


class NodeFind(BaseModel):
    id: Optional[Any]
    short: Optional[Any]
    long: Optional[Any]

class NodeAdd(BaseModel):
    short: str
    long: Optional[str]

class NodeEdit(BaseModel):
    short: Optional[str]
    long: Optional[str]
    contents: Optional[List[Content]]
    external_contents: Optional[List[ExternalContent]]
