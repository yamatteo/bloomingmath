from pydantic import BaseModel, EmailStr, validator, root_validator, ValidationError


class SignupForm(BaseModel):
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


class LoginForm(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_is_not_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Password can't be an empty string.")
        return value
