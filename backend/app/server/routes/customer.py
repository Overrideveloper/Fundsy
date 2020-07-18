from fastapi import APIRouter, Body, Depends, Query, Path, HTTPException, Request
from fastapi.responses import JSONResponse
from app.data.schemas.core import Response, PaginatedResult
from app.data.schemas.customer import CustomerRes, CustomerCreateReq, CustomerGetRes
from app.data.schemas.customer_investment import CustomerInvestmentRes
from app.data.schemas.transaction import TransactionRes
from app.data.repositories.customer import CustomerRepository
from app.data.repositories.customer_investment import CustomerInvestmentRepository
from app.data.repositories.transaction import TransactionRepository
from app.data.database import db
from app.server.middleware.auth import role_access_validator, authorization_validator

router = APIRouter()
customer_repo = CustomerRepository(db)
customer_investment_repo = CustomerInvestmentRepository(db)
transaction_repo = TransactionRepository(db)

@router.post('/signup')
def signup(body: CustomerCreateReq = Body(...)):
    try:
        customer = customer_repo.signup(body)
        data = CustomerRes().dump(customer)
        
        res = Response(data=data, code=201, message="Customer signed up successfully")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except HTTPException as httpexc:
        raise httpexc

@router.get('', dependencies=[Depends(authorization_validator), Depends(role_access_validator(True))])
def get_all(page: int = Query(gt=0, default=None), per_page: int = Query(gt=0, default=None)):
    try:
        dump = CustomerGetRes(many=True).dump
        result = customer_repo.get_all(page, per_page)

        data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)
        res = Response(data=data, code=200, message="Customers returned")
        
        return JSONResponse(content=res.dict(), status_code=res.code)
    except HTTPException as httpexc:
        raise httpexc

@router.get('/{id}', dependencies=[Depends(authorization_validator)])
def get_one(id: int = Path(...)):
    try:
        customer = customer_repo.get_one(id)
        
        if customer:
            res = Response(data=CustomerGetRes().dump(customer), code=200, message="Customer returned");
            return JSONResponse(content=res.dict(), status_code=res.code)
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    except HTTPException as httpexc:
        raise httpexc

@router.get('/{id}/customer_investment', dependencies=[Depends(authorization_validator), Depends(role_access_validator(False))])
def get_customer_investments(request: Request, id: int = Path(...), page: int = Query(gt=0, default=None), per_page: int = Query(gt=0, default=None)):
    try:
        if id != request.state.user["id"]:
            raise HTTPException(status_code=403, detail="Access forbidden")

        dump = CustomerInvestmentRes(many=True).dump
        result = customer_investment_repo.get_by_customer_id(id, page, per_page)

        data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)
        res = Response(data=data, code=200, message="Customer investments returned")
        
        return JSONResponse(content=res.dict(), status_code=res.code)
    except HTTPException as httpexc:
        raise httpexc

@router.get('/{id}/transaction', dependencies=[Depends(authorization_validator)])
def get_customer_transactions(request: Request, id: int = Path(...), page: int = Query(gt=0, default=None), per_page: int = Query(gt=0, default=None)):
    try:
        user = request.state.user

        if id != user["id"] and not user["is_admin"]:
            raise HTTPException(status_code=403, detail="Access forbidden")
        
        dump = TransactionRes(many=True).dump
        result = transaction_repo.get_by_customer_id(id, page, per_page)
        
        data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)
        res = Response(data=data, code=200, message="Customer transactions returned")
        
        return JSONResponse(content=res.dict(), status_code=res.code)
    except HTTPException as httpexc:
        raise httpexc
        