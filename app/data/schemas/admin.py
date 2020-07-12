from pydantic import BaseModel, Field
from marshmallow import Schema, fields
from .user import UserRes

class AdminCreateReq(BaseModel):
    name: str = Field(...)
    username: str = Field(...)
    password: str = Field(..., min_length=7)
    
class AdminRes(Schema):
    id = fields.Int()
    name = fields.Str()
    user_id = fields.Int()
    user = fields.Nested(UserRes)
