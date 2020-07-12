from pydantic import BaseModel, Field

class LoginReq(BaseModel):
    username: str = Field(...)
    password: str = Field(..., min_length=7)

class LoginRes(BaseModel):
    token: str
    data: dict