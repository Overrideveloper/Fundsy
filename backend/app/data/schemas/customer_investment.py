from pydantic import BaseModel, Field
from marshmallow import Schema, fields
from .investment import InvestmentRes

class CustomerInvestmentCreateReq(BaseModel):
    customer_id: int = Field(...)
    title: str = Field(...)
    amount: int = Field(...)
    investment_id: int = Field(...)

class CustomerInvestmentRes(Schema):
    id = fields.Int()
    title = fields.Str()
    amount = fields.Int()
    appreciation = fields.Int()
    created_at = fields.DateTime()
    investment = fields.Nested(InvestmentRes)
    
class CustomerInvestmentResOmitInvestment(Schema):
    id = fields.Int()
    title = fields.Str()
    amount = fields.Int()
    created_at = fields.DateTime()

class CustomerInvestmentWithdrawReq(BaseModel):
    id: int = Field(...)
    amount: int = Field(...)
