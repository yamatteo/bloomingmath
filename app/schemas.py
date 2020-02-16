# Schemas are pydantic models used for validating data and specifying routes' parameters
#
# from pydantic import BaseModel, EmailStr, validator
#
#
# class SignupForm(BaseModel):
#     email: EmailStr
#     password: str
#     password_confirmation: str
#
#     @validator("password")
#     def password_is_not_empty(cls, value):
#         if len(value) == 0:
#             raise ValueError("Password can't be an empty string.")
#         return value