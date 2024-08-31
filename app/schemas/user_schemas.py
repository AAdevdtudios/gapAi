from pydantic import BaseModel, EmailStr, field_validator
from pydantic.fields import Field
import re
from typing import Any

class UserDTO(BaseModel):
    firstname:str = Field(..., min_length=3)
    lastname:str = Field(..., min_length=3)
    username:str= Field(...,min_length=3)
    email:EmailStr
    password_hash:str=Field(min_length=6)

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

class InitiateResetPassword(BaseModel):
    email:EmailStr

class ResetPassword(BaseModel):
    password: str = Field(..., min_length=6)
    confirm_password:str = Field(..., min_length=6)

    @field_validator("password")
    @classmethod
    def regex_match(cls, v) -> str:
        pattern = re.compile(
            r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?=\S+$).{8,20}$'
        )
        if not pattern.match(v):
            raise ValueError("invalid password")
        return v

class ResponseMessage(BaseModel):
    status: int
    message: str
    data: Any = None