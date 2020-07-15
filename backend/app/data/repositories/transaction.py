from fastapi import HTTPException
from sqlalchemy.orm import Session

from data.schemas.transaction import TransactionCreateReq
from data.models.core import Transaction as TransactionModel
from .utils import convertAmountToMinDenomination
from .base import BaseRepository

class TransactionRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        
    def create(self, _transaction: TransactionCreateReq) -> TransactionModel:
        try:
            amount = convertAmountToMinDenomination(_transaction.amount)
            type = _transaction.type
            customer_investment_id = _transaction.customer_investment_id
            customer_id = _transaction.customer_id
            
            transaction = TransactionModel(amount=amount, type=type, customer_investment_id=customer_investment_id, customer_id=customer_id)
            
            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
            
            return transaction
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")

        