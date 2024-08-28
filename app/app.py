from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from .schemas import UserDTO, UserLoginDTO, ResponseMessage
from .services import create_user, get_current_user, get_user_info, login_user, verify_user_token
from .models import User_pydantic

router = APIRouter(tags=["Authentication"])

@router.post("/register",response_model=ResponseMessage,description="This endpoint is used to register a new user and send email verification link for user",)
async def user_registration(user:UserDTO):
    return await create_user(user=user)

@router.post("/login", response_model=ResponseMessage, description="This endpoint is used to generate a token for registered and verified users only",)
async def user_registration(user:UserLoginDTO):
    val= await login_user(userLogin=user)
    content={}
    content["status_code"]=val.status
    content["message"]= val.message
    content["data"]=val.data
    return JSONResponse(status_code=val.status, content=content)

@router.post("/verify-user")
async def verify_user(userId:str,token:str):
    val= await verify_user_token(token=token, userId=userId)
    content={}
    content["status_code"]=val.status
    content["message"]= val.message
    content["data"]=val.data
    return JSONResponse(status_code=val.status, content=content)
