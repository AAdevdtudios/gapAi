from app.schemas.user_schemas import ResetPassword, ResponseMessage
from app.models.dbModels import User, User_pydantic
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.utils.app_utils import generate_reset_password_token, hash_password, generate_verification_token, verify_reset_password_token


# Auth User Services

async def get_user_info(user)->ResponseMessage:
    try:
        return ResponseMessage(message="User Information", status=status.HTTP_200_OK, data=jsonable_encoder(user))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Un authorized user")

async def send_verification_authenticated_user(userId:str):
    try:
        data = await User.get(id=userId)
        if data.verify_user:
            return ResponseMessage(message="User already verified", status=status.HTTP_202_ACCEPTED)
        token = generate_verification_token(userId=data.id)
        return ResponseMessage(message=f"Email sent to user {token}", status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Un authorized user")

async def initiate_reset_password(email:str):
    if not await User.exists(email=email):
        return ResponseMessage(message="Email sent to user if no email was received please check email and request again", status=status.HTTP_200_OK)

    data = await User.get(email=email)
    user = await User_pydantic.from_tortoise_orm(data)
    reset_token = generate_reset_password_token(userId=user.id)
    return ResponseMessage(message=f"Email sent to user {reset_token}", status=status.HTTP_200_OK)

async def reset_password_validation(req:ResetPassword, token:str, userId:str):
    payload = verify_reset_password_token(token=token)
    if not payload["Id"] == userId:
        return ResponseMessage(message="Invalid Information please request for reset", status=status.HTTP_400_BAD_REQUEST)
    if req.password != req.confirm_password:
        return ResponseMessage(message="New password and confirm password doesn't match", status=status.HTTP_400_BAD_REQUEST)
    user =await User.get(id=userId)
    print(user)
    user.password_hash = hash_password(req.password)
    await user.save()
    return ResponseMessage(status=200, message="Password reset confirm",)

# End Auth User Services
