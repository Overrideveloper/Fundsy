from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.responses import JSONResponse
from data.schemas.core import Response, PaginatedResult
from data.schemas.customer_investment import CustomerInvestmentRes, CustomerInvestmentCreateReq
from data.repositories.customer_investment import CustomerInvestmentRepository
from server.middleware.auth import access_validator
from data.database import db

router = APIRouter()
customer_investment_repo = CustomerInvestmentRepository(db)

@router.get('')
def get_all(customer_id: int = Query(..., alias="customer_id"), page: int = Query(alias="page", gt=0, default=None),
            per_page: int = Query(alias="per_page", gt=0, default=None)):
    try:
        dump = CustomerInvestmentRes(many=True).dump
        result = customer_investment_repo.get_by_customer_id(customer_id, page, per_page)

        data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)
        res = Response(data=data, code=200, message="Customer investments returned")
        
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc
    
@router.post('', dependencies=[Depends(access_validator(False))])
def create(body: CustomerInvestmentCreateReq = Body(...)):
    try:
        customer_investment = customer_investment_repo.create(body)
        data = CustomerInvestmentRes().dump(customer_investment)
        
        res = Response(data=data, code=201, message="Customer investment created successfully")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc
    