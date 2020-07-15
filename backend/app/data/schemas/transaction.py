from pydantic import BaseModel, Field
from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField
from decimal import Decimal

from .customer_investment import CustomerInvestmentRes, CustomerInvestmentResOmitInvestment
from data.models.base import TransactionType

class TransactionCreateReq(BaseModel):
    amount: Decimal = Field(...)
    type: TransactionType = Field(...)
    customer_investment_id: int = Field(...)
    customer_id: int = Field(...)

class TransactionRes(Schema):
    id = fields.Int()
    amount = fields.Int()
    type = EnumField(TransactionType, by_value=True)
    customer_investment_id = fields.Int()
    customer_id = fields.Int()
    customer_investment = fields.Nested(CustomerInvestmentResOmitInvestment)
    created_at = fields.DateTime()
    