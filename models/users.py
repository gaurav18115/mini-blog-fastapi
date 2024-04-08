from pydantic import BaseModel


class UserSignup(BaseModel):
    username: str
    email: str
    password: str


class UserSignin(BaseModel):
    username: str
    password: str


class UpdateProfile(BaseModel):
    username: str
    email: str
    bio: str
