from .schemas import ResponseMessage, UserDTO, UserLoginDTO
from .models import User, User_pydantic
from fastapi import HTTPException, status
from tortoise.expressions import Q
from .utils import hash_password, verify_password, generate_verification_token, verify_verification_token, generate_login_token

async def create_user(user: UserDTO) -> ResponseMessage:
    try:
        # Hash the password once and store it as a string (decoded to utf-8)
        hashed_password = hash_password(user.password_hash)

        dataUser = User(
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            password_hash=hashed_password  # Store the hashed password as a string
        )
        await dataUser.save()
        token = generate_verification_token(userId=dataUser.id)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Server error. Please wait while this information is addressed.")

    return ResponseMessage(message=f"Success! Please check your email to verify. {token}", status=status.HTTP_200_OK)
    # return ResponseMessage(message=str(token), status=status.HTTP_200_OK)

async def login_user(userLogin: UserLoginDTO) -> ResponseMessage:
    try:
        user = await User.get(Q(username=userLogin.username) | Q(email=userLogin.username))
        val = verify_password(userLogin.password_hash, user.password_hash)
        if not val:
            return ResponseMessage(message="Invalid credentials", status=status.HTTP_400_BAD_REQUEST)

        userInfo = await User_pydantic.from_tortoise_orm(user)
        return ResponseMessage(message="Login successful", status=200, data={'access_token': generate_login_token(user={**userInfo.model_dump_json()})})
    except Exception as e:
        print(e)
        return ResponseMessage(message="Invalid credentials", status=status.HTTP_404_NOT_FOUND)

async def verify_user_token(userId:str, token:str)->ResponseMessage:
    try:
        user =await User.get(id=userId)
        if user.verify_user:
            return ResponseMessage(message="User already verified please login", status=status.HTTP_400_BAD_REQUEST)
        verify_verification_token(token=token)
        user.verify_user = True
        await user.save()
        return ResponseMessage(status=200, message="User verified please login to continue",)
    except:
        return ResponseMessage(message="Invalid credentials", status=status.HTTP_404_NOT_FOUND)
