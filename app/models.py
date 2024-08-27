from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from .utils import verify_password
from datetime import timedelta

class User(Model):
    id = fields.IntField(primary_key=True)
    firstname= fields.CharField(max_length=100)
    lastname=fields.CharField(max_length=100)
    username= fields.CharField(max_length=50, unique=True)
    email= fields.CharField(max_length=50, unique=True)
    password_hash= fields.CharField(max_length=250)
    verify_user = fields.BooleanField(default=False)
    created = fields.DatetimeField(auto_now_add=True)
    update = fields.DatetimeField(auto_now=True)

    def __str__(self) -> str:
        return self.username

class AiData(Model):
    id = fields.IntField(primary_key=True)
    name= fields.CharField(max_length = 50)
    description = fields.CharField(max_length=250)
    # response = fields.JSONField()
    # response_message= fields.CharField(max_length = 250)
    owner = fields.ForeignKeyField("models.User", related_name="projects", on_delete=fields.CASCADE)


User_pydantic = pydantic_model_creator(User, name = "User", exclude={"password_hash",})
User_pydanticIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)