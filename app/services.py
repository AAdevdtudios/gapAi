from .schemas import ResetPassword, ResponseMessage, UserDTO, UserLoginDTO
from .models import User, User_pydantic
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from tortoise.expressions import Q
from .utils import generate_reset_password_token, hash_password, verify_login_token, verify_password, generate_verification_token, verify_reset_password_token, verify_verification_token, generate_login_token

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
# Create A New User
async def create_user(user: UserDTO) -> ResponseMessage:
    try:
        # Hash the password once and store it as a string (decoded to utf-8)
        hashed_password = hash_password(user.password_hash)
        if await User.exists(Q(username=user.username) | Q(email=user.email)):
            return ResponseMessage(message="Invalid Credentials", status=status.HTTP_400_BAD_REQUEST)

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

# Login user
async def login_user(userLogin: UserLoginDTO) -> ResponseMessage:
    try:
        user = await User.get(Q(username=userLogin.username) | Q(email=userLogin.username))
        val = verify_password(userLogin.password_hash, user.password_hash)
        if not val:
            return ResponseMessage(message="Invalid credentials", status=status.HTTP_400_BAD_REQUEST)
        return ResponseMessage(message="Login successful", status=200, data={'access_token': generate_login_token(user=user.id)})
    except Exception as e:
        print(e)
        return ResponseMessage(message="Invalid credentials", status=status.HTTP_404_NOT_FOUND)

# Verify new User
async def verify_user_token(userId:str, token:str)->ResponseMessage:
    try:
        payload = verify_verification_token(token=token)
        if not payload["Id"] == userId:
            return ResponseMessage(message="Invalid Information please request for reset", status=status.HTTP_400_BAD_REQUEST)
        user =await User.get(id=userId)
        if user.verify_user:
            return ResponseMessage(message="User already verified please login", status=status.HTTP_400_BAD_REQUEST)

        user.verify_user = True
        await user.save()
        return ResponseMessage(status=200, message="User verified please login to continue",)
    except:
        return ResponseMessage(message="Invalid credentials", status=status.HTTP_404_NOT_FOUND)

# Get authenticated User
async def get_current_user(token: str=Depends(oauth2_schema)):
    return verify_login_token(token=token)

async def get_user_info(userId:str)->ResponseMessage:
    try:
        data = await User.get(id=userId)
        user = await User_pydantic.from_tortoise_orm(data)
        return ResponseMessage(message="User Information", status=status.HTTP_200_OK, data=user.model_dump())
    except Exception as e:
        print(e)
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