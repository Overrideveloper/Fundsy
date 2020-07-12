from pydantic import BaseModel, Field
from marshmallow import Schema, fields

class InvestmentReq(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    appreciation_amount: int = Field(..., gt=0)
    appreciation_duration: int = Field(..., gt=0)
    lock_period: int = Field(..., gt=0)
    withdrawal_cost: int = Field(..., gt=0)

class InvestmentRes(Schema):
    id = fields.Int()
    title = fields.Str()
    appreciation_amount = fields.Int()
    appreciation_duration = fields.Int()
    lock_period = fields.Int()
    withdrawal_cost = fields.Int()
