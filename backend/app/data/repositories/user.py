from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .base import BaseRepository
from data.schemas.user import UserReq
from data.models.core import User as UserModel
from fastapi import HTTPException
from .utils import hash_password

class UserRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
    
    def get_by_username(self, username: str) -> UserModel:
        return self.db.query(UserModel).filter(UserModel.username == username).first()
        
    def create(self, _user: UserReq, is_admin=False) -> UserModel:
        try:
            user = UserModel(username=_user.username, hash=hash_password(_user.password), is_admin=is_admin);

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return user
        except IntegrityError as err:
            self.db.rollback()
            raise HTTPException(status_code=422, detail="Username already in use")
        except:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
