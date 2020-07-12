from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from data.schemas.core import Response
from data.schemas.auth import LoginReq, LoginRes
from data.repositories.auth import AuthRepository
from data.database import db

router = APIRouter()
auth_repo = AuthRepository(db)

@router.post('/login')
def signup(body: LoginReq = Body(...)):
    try:
        data, token = auth_repo.login(body)

        res = Response(data=LoginRes(token=token, data=data), code=200, message="Sign in successful")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as err:
        raise err
