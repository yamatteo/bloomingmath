from typing import List

from fastapi import APIRouter, Form, Depends, HTTPException
from pydantic import ValidationError

from extensions.security import get_password_hash, create_access_token
from models import User, Content, Group, Node
from routers import get_current_user, admin_only
from schemas import *

router = APIRouter()


@router.api_route("/current", methods=["GET", "OPTIONS", "POST"])
async def get_current_user(current_user: User = Depends(get_current_user)):
    all_groups = await Group.find()
    cu_groups = await Group.find({"members._id": current_user.id})
    # available_groups = await Group.find({"$not": {"members._id": ObjectId(current_user.id)}})
    available_groups = await Group.find({"members._id": {"$not": {"$eq": current_user.id}}})
    nodes_ids = [node.id for group in cu_groups for node in group.nodes]
    cu_nodes = await Node.find({"id": {"$in": nodes_ids}})
    for node in cu_nodes:
        node.contents = await Content.find({"id": {"$in": [content.id for content in node.contents]}})
    result = current_user.export()
    result["groups"] = [group.export() for group in cu_groups]
    result["nodes"] = [node.export() for node in cu_nodes]
    result["available_groups"] = available_groups
    return result


@router.post("/login")
async def login(user_login: UserLogin):
    try:
        user: Optional[User] = await User.find_one({"email": user_login.email})
        assert user.authenticate(user_login.password)
        access_token = create_access_token(
            data={"sub": user.id}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except (ValidationError, KeyError, AttributeError, AssertionError):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"Authorization": "Bearer"},
        )


@router.post("/urlencode_login")
async def urlencode_login(username: str = Form(...), password: str = Form(...)):
    login_form = UserLogin(email=username, password=password)
    print(login_form)
    try:
        user: Optional[User] = await User.find_one({"email": login_form.email})
        assert user.authenticate(login_form.password)
        access_token = create_access_token(
            data={"sub": user.id}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except (ValidationError, KeyError, AttributeError, AssertionError):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password.",
            headers={"Authorization": "Bearer"},
        )


@router.post("/signup")
async def signup(user_signup: UserSignup):
    try:
        user: Optional[User] = await User.find_one({"email": user_signup.email})
        assert user is None
        await User.insert_one({
            "email": user_signup.email,
            "password_hash": get_password_hash(user_signup.password),
        })
        user: User = await User.find_one({"email": user_signup.email})
        access_token = create_access_token(
            data={"sub": user.id}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except (ValidationError, KeyError, AttributeError, AssertionError):
        raise HTTPException(status_code=400, detail="Invalid data (maybe a duplicate?)")


@router.api_route("/browse", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def browse_users() -> List[User]:
    return await User.find()


@router.api_route("/read", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def read_user(find: UserFindOne) -> Optional[User]:
    return await User.find_one(find=find.dict(exclude_unset=True))


@router.api_route("/add", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def add_user(data: UserAdd) -> User:
    return await User.insert_one({
        "email": data.email,
        "password_hash": get_password_hash(data.password),
        "is_admin": data.is_admin,
        "is_blocked": data.is_blocked
    })


@router.api_route("/edit", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def edit_user(find: UserFindOne, data: UserEdit) -> User:
    find = find.dict(exclude_unset=True)
    data = data.dict(exclude_unset=True)
    if "password" in data.keys():
        data["password_hash"] = get_password_hash(data["password"])
        del data["password"]
    return await User.find_one_and_set(find=find, data=data)


@router.api_route("/delete", methods=["GET", "POST"], dependencies=[Depends(admin_only)])
async def delete_user(find: UserFindOne) -> None:
    find = find.dict(exclude_unset=True)
    await User.delete_one(find=find)
