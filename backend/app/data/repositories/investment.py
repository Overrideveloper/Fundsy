from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, noload
from .base import BaseRepository
from typing import List, Union
from data.schemas.investment import InvestmentReq
from data.models.core import Investment as InvestmentModel

class InvestmentRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        
    def create(self, _investment: InvestmentReq) -> InvestmentModel:
        try:
            investment = InvestmentModel(title=_investment.title, appreciation_amount=_investment.appreciation_amount, appreciation_duration=_investment.appreciation_duration, lock_period=_investment.lock_period, withdrawal_cost=_investment.withdrawal_cost)

            self.db.add(investment)
            self.db.commit()
            self.db.refresh(investment)

            return investment
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def update(self, _investment: InvestmentReq) -> InvestmentModel:
        try:
            investment = self.db.query(InvestmentModel).get(_investment.id)
            
            if not investment:
                raise HTTPException(status_code=404, detail="Investment not found")
            
            investment.title = _investment.title
            investment.appreciation_amount=_investment.appreciation_amount
            investment.appreciation_duration=_investment.appreciation_duration
            investment.lock_period=_investment.lock_period
            investment.withdrawal_cost=_investment.withdrawal_cost

            self.db.commit()
            self.db.refresh(investment)
            
            return investment
        except HTTPException as httpexc:
            raise httpexc
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        
    def delete(self, id: int) -> None:
        try:
            query = self.db.query(InvestmentModel).filter(InvestmentModel.id == id)
            investment = query.first()

            if not investment:
                raise HTTPException(status_code=404, detail="Investment not found")
            else:
                query.delete()
                self.db.commit()
        except HTTPException as httpexc:
            raise httpexc
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
            
    def get_one(self, id: int) -> InvestmentModel:
        try:
            return self.db.query(InvestmentModel).options(noload(InvestmentModel.customer_investments)).get(id)
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def get_all(self, page: int=None, per_page: int=None) -> Union[List[InvestmentModel], tuple]:
        try:
            query = self.db.query(InvestmentModel).options(noload(InvestmentModel.customer_investments)).order_by(InvestmentModel.title.asc())

            if page and per_page:
                offset = (page - 1) * per_page
                
                total = self.db.query(func.count(InvestmentModel.id)).scalar()
                records = query.limit(per_page).offset(offset).all()
                
                return total, records
            else:
                return query.all()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
            