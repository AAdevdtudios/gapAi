# import bcrypt
from passlib.hash import pbkdf2_sha256
import jwt
import time
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from decouple import config

from app.models.dbModels import User, User_pydantic

VERIFICATION_SECRETE_KEY=config("VERIFICATION_SECRETE_KEY")
LOGIN_SECRETE_KEY = config("LOGIN_SECRETE_KEY")
HASHING_SECRETE_KEY=config("HASHING_SECRETE_KEY")
RESET_TOKEN_SECRETE_KEY = config("RESET_TOKEN_SECRETE_KEY")


def hash_password(password: str):
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)

# Generate verification token
def generate_verification_token(userId):
    expiration = int(time.time()) + (24 * 60 * 60)
    data = jsonable_encoder({"Id": userId, "exp": expiration})
    token = jwt.encode(data, key=VERIFICATION_SECRETE_KEY, algorithm="HS256")
    url = f"/verify-user?token={token}&userId={userId}"
    return url

# Verify your token
def verify_verification_token(token):
    try:
        payload = jwt.decode(token, key=VERIFICATION_SECRETE_KEY, algorithms="HS256")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid url or wrong token.")
    except:
        raise HTTPException(status_code=400, detail="Error")

def generate_login_token(user:str)->str:
    payload = {
        "user": user,
        "exp": time.time() + 900
    }
    return jwt.encode(payload=jsonable_encoder(payload), key=LOGIN_SECRETE_KEY, algorithm="HS256")

# Check if user is Authenticated
async def verify_login_token(token:str):
    try:
        payload = jwt.decode(token, LOGIN_SECRETE_KEY, algorithms="HS256")
        user = await User.get(id=payload.get("user"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid url or wrong token.")
    except:
        raise HTTPException(status_code=400, detail="Error")
    return await User_pydantic.from_tortoise_orm(user)

# Generate reset Password token
def generate_reset_password_token(userId):
    expiration = int(time.time()) + (30 * 60)
    data = jsonable_encoder({"Id": userId, "exp": expiration})
    token = jwt.encode(data, key=RESET_TOKEN_SECRETE_KEY, algorithm="HS256")
    url = f"/reset-password?token={token}&userId={userId}"
    return url

# Verify your token
def verify_reset_password_token(token):
    try:
        payload = jwt.decode(token, key=RESET_TOKEN_SECRETE_KEY, algorithms="HS256")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid url or wrong token.")
    except:
        raise HTTPException(status_code=400, detail="Error")