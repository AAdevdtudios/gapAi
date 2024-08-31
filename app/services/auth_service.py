from fastapi import HTTPException, status
from app.models.dbModels import User
from app.schemas.user_schemas import ResponseMessage, UserDTO, UserLoginDTO
from app.utils.app_utils import generate_login_token, generate_verification_token, hash_password, verify_password, verify_verification_token
from tortoise.expressions import Q

# Create/Register New User
async def create_user(user: UserDTO) -> ResponseMessage:
    try:
        # Hash the password once and store it as a string (decoded to utf-8)
        hashed_password = hash_password(user.password_hash)
        if await User.exists(Q(username=user.username) | Q(email=user.email)):
            return ResponseMessage(message="Invalid Credentials", status=status.HTTP_400_BAD_REQUEST)

        dataUser = User(
            username=user.username.lower(),
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email.lower(),
            password_hash=hashed_password  # Store the hashed password as a string
        )
        await dataUser.save()
        token = generate_verification_token(userId=dataUser.id)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Server error. Please wait while this information is addressed.")

    return ResponseMessage(message=f"Success! Please check your email to verify. {token}", status=status.HTTP_200_OK)
    # return ResponseMessage(message=str(token), status=status.HTTP_200_OK)

# Login authenticated User
async def login_user(userLogin: UserLoginDTO) -> ResponseMessage:
    try:
        user = await User.get(Q(username=userLogin.username.lower()) | Q(email=userLogin.username.lower()))
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

# App Services Ended