from fastapi import APIRouter, Body, Query
from fastapi.responses import JSONResponse
from data.schemas.core import Response
from data.schemas.auth import LoginReq, LoginRes, RefreshTokenReq, InvalidateTokenReq
from data.repositories.auth import AuthRepository
from data.database import db

router = APIRouter()
auth_repo = AuthRepository(db)

@router.post('/login')
def login(body: LoginReq = Body(...)):
    try:
        data, auth_token, refresh_token = auth_repo.login(body)

        res = Response(data=LoginRes(auth_token=auth_token, refresh_token=refresh_token, data=data), code=200, message="Sign in successful")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc

@router.post('/refresh_token')
def refresh_token(body: RefreshTokenReq = Body(...)):
    try:
        auth_token = auth_repo.refresh_token(body)
        res = Response(data=auth_token, code=200, message="Token refreshed")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc

@router.post('/invalidate_token')
def refresh_token(body: InvalidateTokenReq = Body(...)):
    try:
        auth_repo.invalidate_token(body.refresh_token)
        res = Response(data=True, code=200, message="Token invalidated")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc

@router.get('/check_user_exists')
def check_user_exists(username: str = Query(..., alias="username")):
    try:
        flag = auth_repo.check_user_exists(username)
        msg = "User exists" if flag else "User does not exist"
        res = Response(data=flag, code=200, message=msg)

        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc
