from fastapi import HTTPException
from sqlalchemy.orm import Session, noload
from sqlalchemy import func
from typing import List, Union
from decimal import Decimal

from data.schemas.customer_investment import CustomerInvestmentCreateReq
from data.schemas.transaction import TransactionCreateReq
from data.schemas.appreciation_log import AppreciationLogCreateReq
from data.models.core import CustomerInvestment as CustomerInvestmentModel
from data.models.base import TransactionType
from .utils import convertAmountToMinDenomination
from .base import BaseRepository
from .transaction import TransactionRepository
from .customer import CustomerRepository
from .investment import InvestmentRepository
from .appreciation_log import AppreciationLogRepository

class CustomerInvestmentRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.transaction_repo = TransactionRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.investment_repo = InvestmentRepository(db)
        self.appreciation_log_repo = AppreciationLogRepository(db)
    
    def create(self, _customer_investment: CustomerInvestmentCreateReq) -> CustomerInvestmentModel:
        try:
            title = _customer_investment.title
            amount = convertAmountToMinDenomination(_customer_investment.amount)
            investment_id = _customer_investment.investment_id
            customer_id = _customer_investment.customer_id
            
            customer = self.customer_repo.get_one(customer_id)
            investment = self.investment_repo.get_one(investment_id)
            
            if not customer:
                raise HTTPException(status_code=404, detail="Customer not found")
            
            if not investment:
                raise HTTPException(status_code=404, detail="Investment not found")
            
            customer_investment = CustomerInvestmentModel(title=title, amount=amount, investment_id=investment_id, customer_id=customer_id)
            
            self.db.add(customer_investment)
            self.db.commit()
            self.db.refresh(customer_investment)
            
            transaction_req = TransactionCreateReq(amount=_customer_investment.amount, type=TransactionType.CREDIT,
                                                   customer_investment_id=customer_investment.id, customer_id=customer_id)
            
            self.transaction_repo.create(transaction_req)

            return customer_investment
        except HTTPException as httpexc:
            raise httpexc
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        
    def get_by_customer_id(self, id: int, page: int=None, per_page: int=None) -> Union[List[CustomerInvestmentModel], tuple]:
        try:
            query = self.db.query(CustomerInvestmentModel).options(noload(CustomerInvestmentModel.customer)).options(noload(CustomerInvestmentModel.transactions)).options(noload(CustomerInvestmentModel.appreciation_logs))
            filteredQuery = query.filter(CustomerInvestmentModel.customer_id == id).order_by(CustomerInvestmentModel.created_at.desc())

            if page and per_page:
                offset = (page - 1) * per_page
                
                total = filteredQuery.count()
                records = filteredQuery.limit(per_page).offset(offset).all()
                
                return total, records
            else:
                return filteredQuery.all()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def get_all(self) -> List[CustomerInvestmentModel]:
        try:
            query = self.db.query(CustomerInvestmentModel).options(noload(CustomerInvestmentModel.customer)).options(noload(CustomerInvestmentModel.transactions)).options(noload(CustomerInvestmentModel.appreciation_logs)).order_by(CustomerInvestmentModel.created_at.desc())

            return query.all()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
   
    def appreciate(self, id:int, appreciation: Decimal) -> CustomerInvestmentModel:
        try:
            customer_investment = self.db.query(CustomerInvestmentModel).get(id)
            
            if not customer_investment:
                raise HTTPException(status_code=404, detail="Customer Investment not found")
            
            new_appreciation = customer_investment.appreciation + appreciation
            appreciation_log = AppreciationLogCreateReq(old_amount=customer_investment.appreciation, new_amount=new_appreciation, customer_investment_id=id)
            customer_investment.appreciation = new_appreciation
            
            self.db.commit()
            self.db.refresh(customer_investment)
            
            self.appreciation_log_repo.create(appreciation_log)
            
            return customer_investment
        except HTTPException as httpexc:
            raise httpexc
        except Exception as exc:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
      