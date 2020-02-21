from typing import Optional

from pydantic import BaseModel, EmailStr, validator, root_validator


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


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_is_not_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Password can't be an empty string.")
        return value


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
