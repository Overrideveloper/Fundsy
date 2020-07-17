from fastapi import HTTPException
from sqlalchemy.orm import Session, noload
from typing import List, Union

from data.schemas.customer_investment import CustomerInvestmentCreateReq
from data.schemas.transaction import TransactionCreateReq
from data.schemas.appreciation_log import AppreciationLogCreateReq
from data.models.core import CustomerInvestment
from data.models.base import TransactionType
from common.utils import convert_datetime_to_unix_timestamp, current_time_unix
from .utils import convert_amount_to_min_denomination
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
    
    def create(self, _customer_investment: CustomerInvestmentCreateReq) -> CustomerInvestment:
        try:
            title = _customer_investment.title
            amount = convert_amount_to_min_denomination(_customer_investment.amount)
            investment_id = _customer_investment.investment_id
            customer_id = _customer_investment.customer_id

            if amount < convert_amount_to_min_denomination(1000):
                raise HTTPException(status_code=422, detail="Minimum investment amount is 1000")

            customer = self.customer_repo.get_one(customer_id)
            investment = self.investment_repo.get_one(investment_id)
            
            if not customer:
                raise HTTPException(status_code=404, detail="Customer not found")
            
            if not investment:
                raise HTTPException(status_code=404, detail="Investment not found")
            
            customer_investment = CustomerInvestment(title=title, amount=amount, investment_id=investment_id, customer_id=customer_id)
            
            self.db.add(customer_investment)
            self.db.commit()
            self.db.refresh(customer_investment)
            
            transaction_req = TransactionCreateReq(amount=amount, type=TransactionType.CREDIT, description="Investment capital",
                                                   customer_investment_id=customer_investment.id, customer_id=customer_id)
            
            self.transaction_repo.create(transaction_req)

            return customer_investment
        except HTTPException as httpexc:
            self.db.rollback()
            raise httpexc
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        
    def get_by_customer_id(self, customer_id: int, page: int=None, per_page: int=None) -> Union[List[CustomerInvestment], tuple]:
        try:
            query = self.db.query(CustomerInvestment).options(noload(CustomerInvestment.customer)).options(noload(CustomerInvestment.transactions)).options(noload(CustomerInvestment.appreciation_logs))
            filteredQuery = query.filter(CustomerInvestment.customer_id == customer_id).order_by(CustomerInvestment.created_at.desc())

            if page and per_page:
                offset = (page - 1) * per_page
                
                total = filteredQuery.count()
                records = filteredQuery.limit(per_page).offset(offset).all()
                
                return total, records
            else:
                return filteredQuery.all()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def get_one(self, id: int, requesting_user_id: int) -> CustomerInvestment:
        try:
            query = self.db.query(CustomerInvestment).options(noload(CustomerInvestment.customer)).options(noload(CustomerInvestment.transactions)).options(noload(CustomerInvestment.appreciation_logs))
            customer_investment = query.get(id)
            
            if not customer_investment:
                raise HTTPException(status_code=404, detail="Customer investment not found")
            
            if requesting_user_id != customer_investment.customer_id:
                raise HTTPException(status_code=403, detail="Access forbidden")

            return customer_investment
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
     
    def get_all(self) -> List[CustomerInvestment]:
        try:
            query = self.db.query(CustomerInvestment).options(noload(CustomerInvestment.customer)).options(noload(CustomerInvestment.transactions)).options(noload(CustomerInvestment.appreciation_logs)).order_by(CustomerInvestment.created_at.desc())

            return query.all()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
   
    def appreciate(self, id:int, appreciation: int) -> CustomerInvestment:
        try:
            customer_investment = self.db.query(CustomerInvestment).get(id)
            
            if not customer_investment:
                raise HTTPException(status_code=404, detail="Customer Investment not found")
            
            new_appreciation = customer_investment.appreciation + appreciation
            
            old_amount = customer_investment.amount + customer_investment.appreciation
            new_amount = customer_investment.amount + new_appreciation
            
            appreciation_log = AppreciationLogCreateReq(old_amount=old_amount, new_amount=new_amount, customer_investment_id=id)
            customer_investment.appreciation = new_appreciation
            
            self.db.commit()
            self.db.refresh(customer_investment)
            
            self.appreciation_log_repo.create(appreciation_log)
            
            return customer_investment
        except HTTPException as httpexc:
            raise httpexc
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def withdrawal_eligibility(self, id: int) -> bool:
        try:
            customer_investment = self.db.query(CustomerInvestment).get(id)

            if not customer_investment:
                raise HTTPException(status_code=404, detail="Customer Investment not found")
            
            return self.get_withdrawal_eligbility(customer_investment)
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def max_amount_withdrawable(self, id: int) -> int:
        try:
            customer_investment = self.db.query(CustomerInvestment).get(id)
            
            if not customer_investment:
                raise HTTPException(status_code=404, detail="Customer Investment not found")

            return self.get_max_amount_withdrawable(customer_investment)
        except HTTPException as httpexc:
            raise httpexc
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")

    def withdraw(self, id: int, requesting_user_id: int, amount: int) -> int:
        try:
            customer_investment = self.db.query(CustomerInvestment).get(id)
            
            if not customer_investment:
                raise HTTPException(status_code=404, detail="Customer Investment not found")
            
            if requesting_user_id != customer_investment.customer_id:
                raise HTTPException(status_code=403, detail="Access forbidden")
            
            withdrawal_eligibility = self.get_withdrawal_eligbility(customer_investment)          
            max_amount_withdrawable = self.get_max_amount_withdrawable(customer_investment)
            
            if withdrawal_eligibility:
                _amount = convert_amount_to_min_denomination(amount)
                
                if not _amount > max_amount_withdrawable:
                    withdrawal_cost = customer_investment.investment.withdrawal_cost
                    withdrawal_fee = int((withdrawal_cost/100) * _amount)
                    total_deduction = _amount + withdrawal_fee
                
                    if customer_investment.appreciation >= total_deduction:
                        customer_investment.appreciation -= total_deduction
                    else:
                        deduction_from_capital = total_deduction - customer_investment.appreciation
                        
                        customer_investment.appreciation -= customer_investment.appreciation
                        customer_investment.amount -= deduction_from_capital
                    
                    self.db.commit()
                    self.db.refresh(customer_investment)
                    
                    withdrawal_tx = TransactionCreateReq(amount=_amount, type=TransactionType.WITHDRAWAL, description="Withdrawal",
                                                         customer_investment_id=customer_investment.id, customer_id=customer_investment.customer_id)
                    withdrawal_charges_tx = TransactionCreateReq(amount=withdrawal_fee, type=TransactionType.WITHDRAWAL, description="Withdrawal charges",
                                                                 customer_investment_id=customer_investment.id, customer_id=customer_investment.customer_id)
                    
                    self.transaction_repo.create(withdrawal_tx)
                    self.transaction_repo.create(withdrawal_charges_tx)
                    
                    return customer_investment
                else:
                    raise HTTPException(status_code=422, detail="Withdrawal amount is more than maximum withdrawable amount")
            else:
                raise HTTPException(status_code=403, detail="Not eligble for withdrawal")
        except HTTPException as httpexc:
            raise httpexc
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        
    def get_withdrawal_eligbility(self, customer_investment: CustomerInvestment) -> bool:
        created_at = convert_datetime_to_unix_timestamp(customer_investment.created_at)
        lock_period = customer_investment.investment.lock_period
        time_since_created = current_time_unix() - created_at
        
        if time_since_created > lock_period:
            return True
        else:
            return False
        
    def get_max_amount_withdrawable(self, customer_investment: CustomerInvestment) -> int:
        total_amount_available = customer_investment.amount + customer_investment.appreciation
        withdrawal_cost = customer_investment.investment.withdrawal_cost
        max_withdrawal = (100 * total_amount_available)/(withdrawal_cost + 100)
        
        return max_withdrawal
    