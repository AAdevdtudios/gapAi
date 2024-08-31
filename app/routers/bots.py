from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.models.dbModels import User_pydantic
from app.schemas.bot_schwas import BotSchema
from app.services.bots_services import (create_bot_user, get_all_users_bot, get_user_single_bot, update_user_single_bot)
from app.services.generalServices import get_current_user

bots_route=APIRouter(tags=["Bots"], prefix="/bots")

@bots_route.post("/create")
async def create_bots(req:BotSchema, user=Depends(get_current_user)):
  val = await create_bot_user(userId=user.id, req=req)
  return JSONResponse(status_code=val.status, content=val.model_dump())

@bots_route.get("/get-all")
async def get_current_bot(user=Depends(get_current_user)):
  val = await get_all_users_bot(userId=user.id)
  return JSONResponse(status_code=val.status, content=val.model_dump())

@bots_route.get("/{id:str}")
async def get_single_bot(id:str, user=Depends(get_current_user)):
  val = await get_user_single_bot(userId=user.id, botId = id)
  return JSONResponse(status_code=val.status, content=val.model_dump())

@bots_route.put("/update/{id:str}")
async def update_single_bot(id:str, req:BotSchema, user=Depends(get_current_user)):
  val = await update_user_single_bot(user=user, botId=id, req=req)
  return JSONResponse(status_code=val.status, content=val.model_dump())