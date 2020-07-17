from fastapi import HTTPException
from sqlalchemy.orm import Session
from .base import BaseRepository
from .user import UserRepository
from .customer import CustomerRepository
from .admin import AdminRepository
from data.schemas.auth import LoginReq, RefreshTokenReq
from .utils import check_password
from common.utils import sign_jwt
from data.schemas.customer import CustomerRes as Customer
from data.schemas.admin import AdminRes as Admin
from common.services import redis
from uuid import uuid4

class AuthRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.user_repo = UserRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.admin_repo = AdminRepository(db)
        
    def login(self, credentials: LoginReq) -> tuple:
        try:
            user = self.user_repo.get_by_username(credentials.username);

            if user:
                if check_password(user.hash, credentials.password):
                    data = None

                    if user.is_admin:
                        data = Admin().dump(self.admin_repo.get_by_user(user.id))
                        
                        if not data:
                            raise HTTPException(status_code=404, detail="Admin not found")
                    else:
                        data = Customer().dump(self.customer_repo.get_by_user(user.id))
                        
                        if not data:
                            raise HTTPException(status_code=404, detail="Customer not found")
                    
                    auth_token_payload = { "id": data["id"], "user_id": user.id, "is_admin": user.is_admin  }
                    auth_token = sign_jwt(auth_token_payload)
                    refresh_token = uuid4().hex

                    redis.set(refresh_token, auth_token_payload)
                    
                    return data, auth_token, refresh_token
                else:
                    raise HTTPException(status_code=422, detail="Invalid credentials provided")
            else:
                raise HTTPException(status_code=422, detail="Invalid credentials provided")
        except HTTPException as httpexc:
            raise httpexc
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        
    def refresh_token(self, credentials: RefreshTokenReq) -> str:
        try:
            auth_token_payload = redis.get(credentials.refresh_token)
            
            if auth_token_payload:
                if auth_token_payload["user_id"] == credentials.user_id:
                    return sign_jwt(auth_token_payload)
                else:
                    raise HTTPException(status_code=422, detail="Invalid credentials provided")   
            else:
                raise HTTPException(status_code=422, detail="Invalid credentials provided")

        except HTTPException as httpexc:
            raise httpexc
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")
        
    def invalidate_token(self, refresh_token: str) -> None:
        try:
            stored_token = redis.get(refresh_token)
            
            if stored_token: 
                redis.delete(refresh_token)
            else:
                raise HTTPException(status_code=422, detail="Invalid credentials provided")
        except HTTPException as httpexc:
            raise httpexc
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")

    def check_user_exists(self, username: str) -> bool:
        try:
            existing_user = self.user_repo.get_by_username(username);
            return True if existing_user else False
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")