from pydantic import BaseModel, Field
from marshmallow import Schema, fields, validate
from decimal import Decimal

from .customer_investment import CustomerInvestmentRes
from data.models.base import TransactionType

class TransactionCreateReq(BaseModel):
    amount: Decimal = Field(...)
    type: TransactionType = Field(...)
    customer_investment_id: int = Field(...)
    customer_id: int = Field(...)

class TransactionRes(Schema):
    amount = fields.Decimal()
    type = fields.Str(validate=validate.OneOf(["CREDIT", "WITHDRAWAL"]))
    customer_investment_id = fields.Int()
    customer_id = fields.Int()
    customer_investment = fields.Nested(CustomerInvestmentRes)
