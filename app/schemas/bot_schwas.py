from pydantic import BaseModel, Field, field_validator
from enum import IntEnum

class DifficultyLevel(IntEnum):
  easy= 0
  medium= 1
  hard= 2
  extreme= 3

class BotSchema(BaseModel):
  name:str = Field(..., min_length=3)
  description:str = Field(..., min_length=5)
  difficulty: DifficultyLevel