# import bcrypt
from passlib.hash import pbkdf2_sha256
import jwt
import time
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from decouple import config

VERIFICATION_SECRETE_KEY=config("VERIFICATION_SECRETE_KEY")
LOGIN_SECRETE_KEY = config("LOGIN_SECRETE_KEY")
HASHING_SECRETE_KEY=config("HASHING_SECRETE_KEY")

def hash_password(password: str):
    # return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10))
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

def generate_login_token(user)->str:
    return jwt.encode(user, key=LOGIN_SECRETE_KEY, algorithm="HS256")