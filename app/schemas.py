from pydantic import BaseModel, EmailStr, field_validator
from pydantic.fields import Field
import re
from .models import User
from typing import Any

class UserDTO(BaseModel):
    firstname:str = Field(..., min_length=3)
    lastname:str = Field(..., min_length=3)
    username:str= Field(...,min_length=3)
    email:EmailStr
    password_hash:str=Field(min_length=6)

    @field_validator("username")
    def checkUser(cls, v):
        user = User.get(username=v)
        if not user:
            raise ValueError("Username already exist")
        return v

    @field_validator("email")
    def validate_email(cls, v):
        user = User.get(email=v)
        if not user:
            raise ValueError("Email already exist")
        return v

    @field_validator("password_hash")
    @classmethod
    def regex_match(cls, v) -> str:
        pattern = re.compile(
            r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?=\S+$).{8,20}$'
        )
        if not pattern.match(v):
            raise ValueError("invalid password")
        return v

class UserLoginDTO(BaseModel):
    username:str
    password_hash:str=Field(min_length=6)

class ResponseMessage(BaseModel):
    status: int
    message: str
    data: Any = None