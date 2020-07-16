from fastapi import HTTPException
from typing import List, Union
from sqlalchemy.orm import Session, noload
from .base import BaseRepository
from data.models.core import AppreciationLog as AppreciationLogModel
from data.schemas.appreciation_log import AppreciationLogCreateReq

class AppreciationLogRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        
    def create(self, req: AppreciationLogCreateReq) -> AppreciationLogModel:
        try: 
            appreciation_log = AppreciationLogModel(old_amount=req.old_amount, new_amount=req.new_amount, customer_investment_id=req.customer_investment_id)
            
            self.db.add(appreciation_log)
            self.db.commit()
            self.db.refresh(appreciation_log)
            
            return appreciation_log
        except Exception as exc:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        
    def get_by_customer_investment(self, customer_investment_id: int, page: int=None, per_page: int=None) -> Union[List[AppreciationLogModel], tuple]:
        try:
            query = self.db.query(AppreciationLogModel).options(noload(AppreciationLogModel.customer_investment)).filter(AppreciationLogModel.customer_investment_id == customer_investment_id).order_by(AppreciationLogModel.created_at.desc())

            if page and per_page:
                offset = (page - 1) * per_page
                
                total = query.count()
                records = query.limit(per_page).offset(offset).all()
                
                return total, records
            else:
                return query.all()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
