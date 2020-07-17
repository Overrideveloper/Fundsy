from sqlalchemy import Column, Integer, DateTime
import datetime
import enum

def timestamp():
    return datetime.datetime.now(datetime.timezone.utc)

class BaseModel():
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=timestamp)
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=timestamp)

@enum.unique
class TransactionType(enum.Enum):
    CREDIT = "CREDIT"
    WITHDRAWAL = "WITHDRAWAL"
