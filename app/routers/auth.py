from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schemas.user_schemas import ResponseMessage, UserDTO, UserLoginDTO

from app.services.auth_service import create_user, login_user, verify_user_token

auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/register",response_model=ResponseMessage,description="This endpoint is used to register a new user and send email verification link for user",)
async def user_registration(user:UserDTO):
    return await create_user(user=user)

@auth_router.post("/login", response_model=ResponseMessage, description="This endpoint is used to generate a token for registered and verified users only",)
async def user_registration(user:UserLoginDTO):
    val= await login_user(userLogin=user)
    return JSONResponse(status_code=val.status, content=val.model_dump())

@auth_router.post("/verify-user")
async def verify_user(userId:str,token:str):
    val= await verify_user_token(token=token, userId=userId)
    return JSONResponse(status_code=val.status, content=val.model_dump())
