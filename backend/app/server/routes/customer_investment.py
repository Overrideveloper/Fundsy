from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.responses import JSONResponse
from data.schemas.core import Response, PaginatedResult
from data.schemas.customer_investment import CustomerInvestmentRes, CustomerInvestmentCreateReq
from data.schemas.appreciation_log import AppreciationLogRes
from data.repositories.customer_investment import CustomerInvestmentRepository
from data.repositories.appreciation_log import AppreciationLogRepository
from server.middleware.auth import role_access_validator
from data.database import db

router = APIRouter()
customer_investment_repo = CustomerInvestmentRepository(db)
appreciation_log_repo = AppreciationLogRepository(db)
    
@router.post('', dependencies=[Depends(role_access_validator(False))])
def create(body: CustomerInvestmentCreateReq = Body(...)):
    try:
        customer_investment = customer_investment_repo.create(body)
        data = CustomerInvestmentRes().dump(customer_investment)
        
        res = Response(data=data, code=201, message="Customer investment created successfully")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc

@router.get('/{id}/appreciation_log', dependencies=[Depends(role_access_validator(False))])
def get_appreciation_logs(id: int = Path(...), page: int = Query(gt=0, default=None), per_page: int = Query(gt=0, default=None)):
    try:
        dump = AppreciationLogRes(many=True).dump
        result = appreciation_log_repo.get_by_customer_investment(id, page, per_page)

        data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)
        res = Response(data=data, code=200, message="Appreciation logs returned")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc
