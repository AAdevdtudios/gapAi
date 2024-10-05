from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.schemas.user_schemas import InitiateResetPassword, ResetPassword
from app.services.user_services import get_user_info, initiate_reset_password, reset_password_validation, send_verification_authenticated_user
from app.models.dbModels import User_pydantic
from app.services.generalServices import get_current_user

user_router = APIRouter(tags=["User"])

# Get User information
@user_router.get("/me")
async def get_User(user=Depends(get_current_user)):
  val = await get_user_info(user)
  return JSONResponse(status_code=val.status, content=val.model_dump())

# Send verification email to authenticated user only
@user_router.get("/send-email")
async def send_email(user=Depends(get_current_user)):
  val = await send_verification_authenticated_user(userId=user.id)
  return JSONResponse(status_code=val.status, content=val.model_dump())

# Send Reset Password
@user_router.post("/initiate-reset")
async def initiate_reset(req:InitiateResetPassword):
  val = await initiate_reset_password(email=req.email)
  return JSONResponse(status_code=val.status, content=val.model_dump())

# Reset Password form token and id
@user_router.post("/reset-password")
async def reset_password_token(token:str, userId:str, req:ResetPassword):
  val = await reset_password_validation(userId=userId, token=token, req=req)
  return JSONResponse(status_code=val.status, content=val.model_dump())