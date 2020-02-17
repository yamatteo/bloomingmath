from fastapi import APIRouter, Form, Depends, HTTPException
from extensions.security import get_password_hash, create_access_token, decode_token
from models import User, Group, Optional
from schemas import SignupForm, LoginForm, ValidationError
from routers import get_current_user

router = APIRouter()



@router.get("/current/")
async def current_user(current_user: User = Depends(get_current_user)):
    cu_groups = [group.dict() for group in await Group.find({"members": current_user.id})]
    result = current_user.dict()
    result["groups"] = cu_groups
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
