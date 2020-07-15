from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, noload
from typing import List, Union
from .base import BaseRepository
from .user import UserRepository, UserReq
from data.schemas.customer import CustomerCreateReq
from data.models.core import Customer as CustomerModel

class CustomerRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.user_repo = UserRepository(db)
        
    def signup(self, _customer: CustomerCreateReq) -> CustomerModel:
        try:
            user_req = UserReq(username=_customer.username, password=_customer.password)
            user = self.user_repo.create(user_req)
            customer = CustomerModel(name=_customer.name, user_id=user.id)

            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
            
            return customer
        except HTTPException as httpexc:
            raise httpexc
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def get_by_user(self, user_id: int) -> CustomerModel:
        try:
            return self.db.query(CustomerModel).filter(CustomerModel.user_id == user_id).first()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def get_one(self, id: int) -> CustomerModel:
        try:
            return self.db.query(CustomerModel).get(id)
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
            
    def get_all(self, page: int=None, per_page: int=None) -> Union[List[CustomerModel], tuple]:
        try:
            query = self.db.query(CustomerModel).options(noload(CustomerModel.user)).order_by(CustomerModel.name.asc())

            if page and per_page:
                offset = (page - 1) * per_page
                
                total = self.db.query(func.count(CustomerModel.id)).scalar()
                records = query.limit(per_page).offset(offset).all()
                
                return total, records
            else:
                return query.all()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
