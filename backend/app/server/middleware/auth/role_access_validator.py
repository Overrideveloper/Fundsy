from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

class RoleAccessValidator(HTTPBearer):
    def __init__(self, is_admin: bool, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.is_admin = is_admin
    
    async def __call__(self, request: Request):
        user = request.state.user;
        
        if user:
            if self.is_admin:
                if user["is_admin"]:
                    return True
                else:
                    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Access forbidden")
            
            if not self.is_admin:
                if not user["is_admin"]:
                    return True
                else:
                    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Access forbidden")
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization missing or invalid");

def role_access_validator(is_admin: bool) -> RoleAccessValidator:
    return RoleAccessValidator(is_admin)
