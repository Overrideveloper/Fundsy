from pydantic import BaseModel
from marshmallow import Schema, fields

class UserReq(BaseModel):
    username: str
    password: str
    
class UserRes(Schema):
    id = fields.Int()
    username = fields.Str()
    is_admin = fields.Bool()