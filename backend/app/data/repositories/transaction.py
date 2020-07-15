from fastapi import HTTPException
from sqlalchemy.orm import Session, noload
from typing import List, Union

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
        
    def get_by_customer_id(self, id: int, page: int=None, per_page: int=None) -> Union[List[TransactionModel], tuple]:
        try:
            query = self.db.query(TransactionModel).options(noload(TransactionModel.customer)).filter(TransactionModel.customer_id == id).order_by(TransactionModel.created_at.desc())
            
            if page and per_page:
                offset = (page - 1) * per_page
                
                total = query.count()
                records = query.limit(per_page).offset(offset).all()
                
                return total, records
            else:
                return query.all()
        except:
            raise HTTPException(status_code=500, detail="An error occurred. Please try again")
