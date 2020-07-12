from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from common.utils import decodeJWT

class JWTValidator(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization missing or invalid")
            elif not self.authorize(credentials.credentials, request):
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization missing or invalid")
            else:
                return True
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authorization missing or invalid")
    
    def authorize(self, token: str, request: Request) -> bool:
        is_valid = False
        payload = decodeJWT(token)
        
        if payload:
            request.state.user = payload
            is_valid = True
        else:
            is_valid = False
            
        return is_valid

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

authorization_validator = JWTValidator(True)
admin_access_validator = AdminAccessValidator(True)