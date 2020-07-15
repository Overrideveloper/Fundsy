from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from data.schemas.core import Response
from data.schemas.customer_investment import CustomerInvestmentRes, CustomerInvestmentCreateReq
from data.repositories.customer_investment import CustomerInvestmentRepository
from server.middleware.auth import role_access_validator
from data.database import db

router = APIRouter()
customer_investment_repo = CustomerInvestmentRepository(db)
    
@router.post('', dependencies=[Depends(role_access_validator(False))])
def create(body: CustomerInvestmentCreateReq = Body(...)):
    try:
        customer_investment = customer_investment_repo.create(body)
        data = CustomerInvestmentRes().dump(customer_investment)
        
        res = Response(data=data, code=201, message="Customer investment created successfully")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc
