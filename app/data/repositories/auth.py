from fastapi import HTTPException
from sqlalchemy.orm import Session
from .base import BaseRepository
from .user import UserRepository
from .customer import CustomerRepository
from .admin import AdminRepository
from data.schemas.auth import LoginReq
from .utils import checkPassword
from common.utils import signJWT
from data.schemas.customer import CustomerRes as Customer
from data.schemas.admin import AdminRes as Admin

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
                if checkPassword(user.hash, credentials.password):
                    data = None

                    if user.is_admin:
                        data = Admin().dump(self.admin_repo.get_by_user(user.id))
                        
                        if not data:
                            raise HTTPException(status_code=404, detail="Admin not found")
                    else:
                        data = Customer().dump(self.customer_repo.get_by_user(user.id))
                        
                        if not data:
                            raise HTTPException(status_code=404, detail="Customer not found")
                    
                    token_payload = { "id": user.id, "is_admin": user.is_admin  }
                    token = signJWT(token_payload)
                    
                    return data, token
                else:
                    raise HTTPException(status_code=422, detail="Invalid credentials provided")
            else:
                raise HTTPException(status_code=422, detail="Invalid credentials provided")
        except:
            raise HTTPException(status_code=500, detail="An error occured. Please try again")