from fastapi import APIRouter
from .schemas import UserDTO, UserLoginDTO
from .services import create_user, login_user
# from passlib.hash import bcrypt
# import bcrypt

router = APIRouter(tags=["Authentication"])

@router.post("/register")
async def user_registration(user:UserDTO):
    return await create_user(user=user)

@router.post("/login")
async def user_registration(user:UserLoginDTO):
    return await login_user(userLogin=user)

@router.get("/")
def getUser():
    return {"details":"All good with the network"}