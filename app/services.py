from .schemas import ResponseMessage, UserDTO, UserLoginDTO
from .models import User
from fastapi import HTTPException
from tortoise.expressions import Q
from .utils import hash_password, verify_password

async def create_user(user: UserDTO) -> ResponseMessage:
    try:
        # Hash the password once and store it as a string (decoded to utf-8)
        hashed_password = hash_password(user.password_hash).decode('utf-8')

        dataUser = User(
            username=user.username,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            password_hash=hashed_password  # Store the hashed password as a string
        )
        await dataUser.save()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Server error. Please wait while this information is addressed.")

    return ResponseMessage(message="Success! Please check your email to verify.", status=200)

async def login_user(userLogin: UserLoginDTO) -> ResponseMessage:
    try:
        user = await User.get(Q(username=userLogin.username) | Q(email=userLogin.username))
        # Verify the password (re-encode the stored hash back to bytes)
        if not verify_password(userLogin.password_hash, user.password_hash.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="User does not exist please confirm your information")

    return ResponseMessage(message="Login successful", status=200, data={})
