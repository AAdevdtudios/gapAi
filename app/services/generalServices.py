# Get authenticated User
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.dbModels import User_pydantic
from app.utils.app_utils import verify_login_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str=Depends(oauth2_schema)):
    return await verify_login_token(token=token)