from typing import Optional

from fastapi import APIRouter, Form, Depends, HTTPException

from extensions.security import get_password_hash, create_access_token
from models import User, Content, Group, Node
from routers import get_current_user
from schemas import SignupForm, LoginForm, ValidationError

router = APIRouter()


@router.get("/current/")
async def get_current_user(current_user: User = Depends(get_current_user)):
    cu_groups = await Group.find({"members": current_user})
    nodes_ids = [node.id for group in cu_groups for node in group.nodes]
    cu_nodes = await Node.find({"id": {"$in": nodes_ids}})
    for node in cu_nodes:
        node.contents = await Content.find({"id": {"$in": [content.id for content in node.contents]}})
    result = current_user.export()
    result["groups"] = [group.export() for group in cu_groups]
    result["nodes"] = [node.export() for node in cu_nodes]
    return result


@router.post("/login")
async def login(login_form: LoginForm):
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
            detail="Incorrect username or password",
            headers={"Authorization": "Bearer"},
        )


@router.post("/urlencode_login")
async def urlencode_login(username: str = Form(...), password: str = Form(...)):
    login_form = LoginForm(email=username, password=password)
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
async def signup(signup_form: SignupForm):
    try:
        user: Optional[User] = await User.find_one({"email": signup_form.email})
        assert user is None
        await User.insert_one({
            "email": signup_form.email,
            "password_hash": get_password_hash(signup_form.password),
        })
        user: User = await User.find_one({"email": signup_form.email})
        access_token = create_access_token(
            data={"sub": user.id}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except (ValidationError, KeyError, AttributeError, AssertionError):
        raise HTTPException(status_code=400, detail="Invalid data (maybe a duplicate?)")
