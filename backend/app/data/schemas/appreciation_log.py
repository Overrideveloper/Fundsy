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

class AppreciationLogResWeekly(AppreciationLogResDaily):
    week = fields.Int()
    year = fields.Int()

class AppreciationLogResMonthly(AppreciationLogResDaily):
    month = fields.Int()
    year = fields.Int()

class AppreciationLogResQuarterly(AppreciationLogResDaily):
    quarter = fields.Int()
    year = fields.Int()

class AppreciationLogReqQuery(Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
