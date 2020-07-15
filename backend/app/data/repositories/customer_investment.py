from fastapi import HTTPException
from sqlalchemy.orm import Session, noload
from sqlalchemy import func
from typing import List, Union

from data.schemas.customer_investment import CustomerInvestmentCreateReq
from data.schemas.transaction import TransactionCreateReq
from data.models.core import CustomerInvestment as CustomerInvestmentModel
from data.models.base import TransactionType
from .utils import convertAmountToMinDenomination
from .base import BaseRepository
from .transaction import TransactionRepository
from .customer import CustomerRepository
from .investment import InvestmentRepository


class CustomerInvestmentRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.transaction_repo = TransactionRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.investment_repo = InvestmentRepository(db)
    
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
        
    def get_by_customer_id(self, customer_id, page: int=None, per_page: int=None) -> Union[List[CustomerInvestmentModel], tuple]:
        try:
            query = self.db.query(CustomerInvestmentModel).options(noload(CustomerInvestmentModel.customer)).options(noload(CustomerInvestmentModel.transactions)).filter(CustomerInvestmentModel.customer_id == customer_id)

            if page and per_page:
                offset = (page - 1) * per_page
                
                total = query.count()
                records = query.limit(per_page).offset(offset).all()
                
                return total, records
            else:
                return query.all()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
