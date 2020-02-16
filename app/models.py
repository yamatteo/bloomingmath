# Models are classes that inherit
# from extensions.mongo_orm import Model, EmailStr
# from extensions.security import verify_password, get_password_hash
#
#
#
# class User(Model):
#     collection_name = "users"
#     email: EmailStr
#     password_hash: str
#     username: str = ""
#     is_admin: bool = False
#     is_blocked: bool = False
#
#     def authenticate(self, password: str) -> bool:
#         return verify_password(password, self.password_hash)
#
#     def set_password(self, password: str) -> "User":
#         self.password_hash = get_password_hash(password)
#         return self