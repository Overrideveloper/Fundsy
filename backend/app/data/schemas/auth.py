from pydantic import BaseModel, Field

class LoginReq(BaseModel):
    username: str = Field(...)
    password: str = Field(..., min_length=7)

class LoginRes(BaseModel):
    auth_token: str
    refresh_token: str
    data: dict

class RefreshTokenReq(BaseModel):
    user_id: int = Field(...)
    refresh_token: str = Field(...)

class InvalidateTokenReq(BaseModel):
    refresh_token: str = Field(...)
    