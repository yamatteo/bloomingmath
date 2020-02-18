from extensions.mongodb_orm import BareModel as Model
from extensions.mongodb_orm import One, Maybe, Many
from pydantic import EmailStr
from typing import Optional
from extensions.security import verify_password, get_password_hash


class User(Model):
    collection_name = "users"
    email: EmailStr
    password_hash: str
    is_admin: bool = False
    is_blocked: bool = False

    def authenticate(self, password: str) -> bool:
        return verify_password(password, self.password_hash)

    def set_password(self, password: str) -> "User":
        self.password_hash = get_password_hash(password)
        return self


class Node(Model):
    collection_name: str = "nodes"
    short: str
    long: Optional[str] = ""


class Group(Model):
    collection_name = "groups"
    short: str
    long: Optional[str] = ""
    members: Many[User] = []
    nodes: Many[Node] = []