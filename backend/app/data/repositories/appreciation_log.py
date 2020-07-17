from fastapi import HTTPException
from typing import List, Union
from sqlalchemy import extract, select, func, desc, text
from sqlalchemy.orm import Session, noload
from .base import BaseRepository
from data.models.core import AppreciationLog
from data.schemas.appreciation_log import AppreciationLogCreateReq

class AppreciationLogRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        
    def create(self, req: AppreciationLogCreateReq) -> AppreciationLog:
        try: 
            appreciation_log = AppreciationLog(old_amount=req.old_amount, new_amount=req.new_amount, customer_investment_id=req.customer_investment_id)
            
            self.db.add(appreciation_log)
            self.db.commit()
            self.db.refresh(appreciation_log)
            
            return appreciation_log
        except Exception as exc:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        
    def get_by_customer_investment(self, customer_investment_id: int, page: int=None, per_page: int=None) -> Union[List[AppreciationLog], tuple]:
        try:
            query = self.db.query(AppreciationLog).options(noload(AppreciationLog.customer_investment)).filter(AppreciationLog.customer_investment_id == customer_investment_id).order_by(AppreciationLog.created_at.desc())

            if page and per_page:
                offset = (page - 1) * per_page
                
                total = query.count()
                records = query.limit(per_page).offset(offset).all()
                
                return total, records
            else:
                return query.all()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def get_by_customer_investment_weekly(self, customer_investment_id: int, page: int=None, per_page: int=None) -> Union[list, tuple]:
        try:
            res = self.db.execute(
                select([extract("week", AppreciationLog.created_at).label("week"), extract("year", AppreciationLog.created_at).label("year"), func.max(AppreciationLog.created_at).label("created_at"), func.max(AppreciationLog.old_amount).label("old_amount"), func.max(AppreciationLog.new_amount).label("new_amount")]).where(AppreciationLog.customer_investment_id == customer_investment_id).group_by(text("year, week")).order_by(desc(text("year, week")))
            )

            data = []
            
            for row in res:
                data.append(dict(zip(row.keys(), row)))
                
            if page and per_page:
                total = len(data)
                offset = (page - 1) * per_page
                stop = offset + per_page
                
                return total, data[offset:stop]
            else:
                return data
        except Exception as exc:
            print(exc)
            raise HTTPException(status_code=500, detail="An error occured. Please try again")

    def get_by_customer_investment_monthly(self, customer_investment_id: int, page: int=None, per_page: int=None) -> Union[list, tuple]:
        try:
            res = self.db.execute(
                select([extract("month", AppreciationLog.created_at).label("month"), extract("year", AppreciationLog.created_at).label("year"), func.max(AppreciationLog.created_at).label("created_at"), func.max(AppreciationLog.old_amount).label("old_amount"), func.max(AppreciationLog.new_amount).label("new_amount")]).where(AppreciationLog.customer_investment_id == customer_investment_id).group_by(text("year, month")).order_by(desc(text("year, month")))
            )

            data = []
            
            for row in res:
                data.append(dict(zip(row.keys(), row)))
                
            if page and per_page:
                total = len(data)
                offset = (page - 1) * per_page
                stop = offset + per_page
                
                return total, data[offset:stop]
            else:
                return data
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        
    def get_by_customer_investment_quarterly(self, customer_investment_id: int, page: int=None, per_page: int=None) -> Union[list, tuple]:
        try:
            res = self.db.execute(
                select([extract("quarter", AppreciationLog.created_at).label("quarter"), extract("year", AppreciationLog.created_at).label("year"), func.max(AppreciationLog.created_at).label("created_at"), func.max(AppreciationLog.old_amount).label("old_amount"), func.max(AppreciationLog.new_amount).label("new_amount")]).where(AppreciationLog.customer_investment_id == customer_investment_id).group_by(text("year, quarter")).order_by(desc(text("year, quarter")))
            )

            data = []
            
            for row in res:
                data.append(dict(zip(row.keys(), row)))
                
            if page and per_page:
                total = len(data)
                offset = (page - 1) * per_page
                stop = offset + per_page
                
                return total, data[offset:stop]
            else:
                return data
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        