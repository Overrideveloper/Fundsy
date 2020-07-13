from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

class AdminAccessValidator(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        user = request.state.user;
        
        if user:
            if user["is_admin"]:
                return True
            else:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Access forbidden")
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization missing or invalid");

admin_access_validator = AdminAccessValidator(True)