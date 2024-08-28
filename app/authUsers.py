from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.schemas import InitiateResetPassword, ResetPassword
from .services import create_user, get_current_user, get_user_info, initiate_reset_password, login_user, reset_password_validation, send_verification_authenticated_user, verify_user_token
from .models import User_pydantic

auth_router = APIRouter(tags=["User"])
# Get User information
@auth_router.get("/me")
async def get_User(user:User_pydantic=Depends(get_current_user)): # type: ignore
    print(user)
    val = await get_user_info(userId=user["user"])
    return val

# Send verification email to authenticated user only
@auth_router.get("/send-email")
async def send_email(user=Depends(get_current_user)): # type: ignore
  val = await send_verification_authenticated_user(userId=user["user"])
  content={}
  content["message"]= val.message
  content["status_code"] = val.status
  content["data"]=val.data
  return JSONResponse(status_code=val.status, content=content)

# Send Reset Password
@auth_router.post("/initiate-reset")
async def initiate_reset(req:InitiateResetPassword):
  val = await initiate_reset_password(email=req.email)
  content={}
  content["message"]= val.message
  content["status_code"] = val.status
  content["data"]=val.data
  return JSONResponse(status_code=val.status, content=content)

# Reset Password form token and id
@auth_router.post("/reset-password")
async def reset_password_token(token:str, userId:str, req:ResetPassword):
  val = await reset_password_validation(userId=userId, token=token, req=req)
  content={}
  content["message"]= val.message
  content["status_code"] = val.status
  content["data"]=val.data
  return JSONResponse(status_code=val.status, content=content)