from app.models.dbModels import User, AiData, Bot_pydantic, User_pydanticIn
from app.schemas.bot_schwas import BotSchema
from app.schemas.user_schemas import ResponseMessage
from fastapi import status
from fastapi.encoders import jsonable_encoder

async def create_bot_user(userId:str, req:BotSchema):
  if not await User.exists(id=userId):
    return ResponseMessage(message="User doesn't exist", status=status.HTTP_401_UNAUTHORIZED)

  user = await User.get(id=userId)
  if not user.verify_user:
    return ResponseMessage(message="User not verified", status=status.HTTP_400_BAD_REQUEST)
  create_bot = await AiData.create(owner=user, **req.model_dump())
  bot = await Bot_pydantic.from_tortoise_orm(create_bot)
  return ResponseMessage(message="Bot created successfully", status=status.HTTP_201_CREATED, data=jsonable_encoder(bot))

async def get_all_users_bot(userId:str):
  if not await User.exists(id=userId):
    return ResponseMessage(message="User doesn't exist", status=status.HTTP_401_UNAUTHORIZED)

  user = await User.get(id=userId)
  if not user.verify_user:
    return ResponseMessage(message="User not verified", status=status.HTTP_400_BAD_REQUEST)

  item= AiData.filter(owner=user)
  data= await Bot_pydantic.from_queryset(item)

  return ResponseMessage(message="Success", status=status.HTTP_200_OK, data=jsonable_encoder(data))

async def get_user_single_bot(userId:str, botId:str):
  if not await User.exists(id=userId):
    return ResponseMessage(message="User doesn't exist", status=status.HTTP_401_UNAUTHORIZED)

  user = await User.get(id=userId)
  if not user.verify_user:
    return ResponseMessage(message="User not verified", status=status.HTTP_400_BAD_REQUEST)

  item= AiData.get(owner=user, id= botId)
  data= await Bot_pydantic.from_queryset_single(item)

  return ResponseMessage(message="Success", status=status.HTTP_200_OK, data=jsonable_encoder(data))

async def update_user_single_bot(user, botId:str, req:BotSchema):
  if not user.verify_user:
    return ResponseMessage(message="User not verified", status=status.HTTP_400_BAD_REQUEST)

  if not await AiData.exists(id=botId,owner__id=user.id):
    return ResponseMessage(message="Ai bot doesn't exist", status=status.HTTP_400_BAD_REQUEST)

  item = await AiData.get(id=botId)
  item.name = req.name
  item.description = req.description
  await item.save()

  data= await Bot_pydantic.from_tortoise_orm(item)
  return ResponseMessage(message="Success", status=status.HTTP_200_OK, data=jsonable_encoder(data))
