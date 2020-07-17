from pydantic import BaseModel, Field
from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from .customer_investment import CustomerInvestmentRes, CustomerInvestmentResOmitInvestment
from data.models.base import TransactionType

class TransactionCreateReq(BaseModel):
    amount: int
    description: str
    type: TransactionType
    customer_investment_id: int
    customer_id: int

class TransactionRes(Schema):
    id = fields.Int()
    amount = fields.Int()
    description = fields.Str()
    type = EnumField(TransactionType, by_value=True)
    customer_investment_id = fields.Int()
    customer_id = fields.Int()
    customer_investment = fields.Nested(CustomerInvestmentResOmitInvestment)
    created_at = fields.DateTime()
    