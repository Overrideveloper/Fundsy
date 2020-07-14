from fastapi import APIRouter, Body, Depends, Query
from fastapi.responses import JSONResponse
from data.schemas.core import Response, PaginatedResult
from data.schemas.customer import CustomerRes, CustomerCreateReq, CustomerGetRes
from data.repositories.customer import CustomerRepository
from data.database import db
from server.middleware.auth import admin_access_validator, authorization_validator

router = APIRouter()
customer_repo = CustomerRepository(db)
deps = [Depends(authorization_validator), Depends(admin_access_validator)]

@router.post('/signup')
def signup(body: CustomerCreateReq = Body(...)):
    try:
        customer = customer_repo.signup(body)
        data = CustomerRes().dump(customer)
        
        res = Response(data=data, code=201, message="Customer signed up successfully")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as err:
        raise err

@router.get('', dependencies=deps)
def get_all(page: int = Query(alias="page", gt=0, default=None), per_page: int = Query(alias="per_page", gt=0, default=None)):
    try:
        dump = CustomerGetRes(many=True).dump
        result = customer_repo.get_all(page, per_page)

        data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)
        res = Response(data=data, code=200, message="Customers returned")
        
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as err:
        raise err
