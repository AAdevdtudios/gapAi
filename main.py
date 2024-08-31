from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
from app.routers.bots import bots_route
from app.routers.user import user_router
from app.routers.auth import auth_router
from tortoise.contrib.fastapi import register_tortoise
from tortoise_config import TORTOISE_ORM


api = FastAPI(title="GAP api")

api.include_router(bots_route)
api.include_router(router=user_router)
api.include_router(router=auth_router)

@api.exception_handler(RequestValidationError)
async def value_error(request:Request, exc:RequestValidationError):
    val = exc.errors()
    input_req = (lambda x:"password" if x=="password_hash" else x)(val[0]['loc'][-1])
    return JSONResponse(status_code=400, content={"input": input_req,"message": val[0]["msg"] })

register_tortoise(
    app=api,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run("main:api", port=8080, host="127.0.0.1", reload=True)