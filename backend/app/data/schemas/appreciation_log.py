from pydantic import BaseModel, Field
from marshmallow import Schema, fields
from enum import Enum

class AppreciationLogCreateReq(BaseModel):
    old_amount: int
    new_amount: int
    customer_investment_id: int

class AppreciationLogResDaily(Schema):
    old_amount = fields.Int()
    new_amount = fields.Int()
    created_at = fields.Str()

class AppreciationLogResWeekly(Schema):
    week = fields.Int()
    old_amount = fields.Int()
    new_amount = fields.Int()
    created_at = fields.Str()

class AppreciationLogResMonthly(Schema):
    month = fields.Int()
    old_amount = fields.Int()
    new_amount = fields.Int()
    created_at = fields.Str()

class AppreciationLogResQuarterly(Schema):
    quarter = fields.Int()
    old_amount = fields.Int()
    new_amount = fields.Int()
    created_at = fields.Str()

class AppreciationLogReqQuery(Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
