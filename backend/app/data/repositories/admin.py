from fastapi import HTTPException
from sqlalchemy.orm import Session
from .base import BaseRepository
from .user import UserRepository, UserReq
from data.schemas.admin import AdminCreateReq
from data.models.core import Admin as AdminModel

class AdminRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.user_repo = UserRepository(db)
        
    def create(self, _admin: AdminCreateReq) -> AdminModel:
        try:
            user_req = UserReq(username=_admin.username, password=_admin.password)
            user = self.user_repo.create(user_req, True)
            admin = AdminModel(name=_admin.name, user_id=user.id)

            self.db.add(admin)
            self.db.commit()
            self.db.refresh(admin)

            return admin
        except HTTPException as httpexc:
            raise httpexc
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def get_by_user(self, user_id: int) -> AdminModel:
        try:
            return self.db.query(AdminModel).filter(AdminModel.user_id == user_id).first()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
    
    def is_existing_admin(self) -> AdminModel:
        try:
            return self.db.query(AdminModel).first()
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
