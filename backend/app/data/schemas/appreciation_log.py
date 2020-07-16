from pydantic import BaseModel, Field
from marshmallow import Schema, fields
from decimal import Decimal

class AppreciationLogCreateReq(BaseModel):
    old_amount: Decimal
    new_amount: Decimal
    customer_investment_id: int
    
class AppreciationLogRes(Schema):
    id = fields.Int()
    old_amount = fields.Int()
    new_amount = fields.Int()
    customer_investment_id = fields.Int()
    created_at = fields.Str()
