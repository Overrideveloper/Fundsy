from fastapi import APIRouter, Body, Depends, Path, Query, Request, HTTPException
from fastapi.responses import JSONResponse
from app.data.schemas.core import Response, PaginatedResult
from app.data.schemas.customer_investment import CustomerInvestmentRes, CustomerInvestmentCreateReq, CustomerInvestmentWithdrawReq
from app.data.schemas.appreciation_log import AppreciationLogReqQuery, AppreciationLogResDaily, AppreciationLogResQuarterly, AppreciationLogResWeekly, AppreciationLogResMonthly
from app.data.repositories.customer_investment import CustomerInvestmentRepository
from app.data.repositories.appreciation_log import AppreciationLogRepository
from app.server.middleware.auth import role_access_validator
from app.data.database import db
from app.common.config import MIN_WITHDRAWAL

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
    except HTTPException as httpexc:
        raise httpexc

@router.get('/{id}', dependencies=[Depends(role_access_validator(False))])
def get_one(request: Request, id: int = Path(...)):
    try:
        requesting_user_id = request.state.user["id"]

        customer_investment = customer_investment_repo.get_one(id, requesting_user_id)
        data = CustomerInvestmentRes().dump(customer_investment)
        res = Response(data=data, code=200, message="Customer investment returned")

        return JSONResponse(content=res.dict(), status_code=res.code)
    except HTTPException as httpexc:
        raise httpexc

@router.get('/{id}/appreciation_log', dependencies=[Depends(role_access_validator(False))])
def get_appreciation_logs(id: int = Path(...), type: AppreciationLogReqQuery = Query(default=None), page: int = Query(gt=0, default=None), per_page: int = Query(gt=0, default=None)):
    try:
        data = None
        
        if type == AppreciationLogReqQuery.WEEKLY:
            result = appreciation_log_repo.get_by_customer_investment_weekly(id, page, per_page)
            dump = AppreciationLogResWeekly(many=True).dump
            data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)
        elif type == AppreciationLogReqQuery.MONTHLY:
            result = appreciation_log_repo.get_by_customer_investment_monthly(id, page, per_page)
            dump = AppreciationLogResMonthly(many=True).dump
            data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)
        elif type == AppreciationLogReqQuery.QUARTERLY:
            result = appreciation_log_repo.get_by_customer_investment_quarterly(id, page, per_page)
            dump = AppreciationLogResQuarterly(many=True).dump
            data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)
        else:
            result = appreciation_log_repo.get_by_customer_investment(id, page, per_page)
            dump = AppreciationLogResDaily(many=True).dump
            data = PaginatedResult(data=dump(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump(result)

        res = Response(data=data, code=200, message="Appreciation logs returned")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except HTTPException as httpexc:
        raise httpexc

@router.get('/{id}/withdrawal_eligibility', dependencies=[Depends(role_access_validator(False))])
def get_withdrawal_eligibility(id: int = Path(...)):
    try:
        data = customer_investment_repo.withdrawal_eligibility(id)
        res = Response(data=data, code=200, message="Withdrawal eligibility returned")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except HTTPException as httpexc:
        raise httpexc

@router.get('/{id}/max_amount_withdrawable', dependencies=[Depends(role_access_validator(False))])
def get_withdrawal_eligibility(id: int = Path(...)):
    try:
        data = customer_investment_repo.max_amount_withdrawable(id)
        res = Response(data=data, code=200, message="Max amount withdrawable returned")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except HTTPException as httpexc:
        raise httpexc

@router.post('/withdraw', dependencies=[Depends(role_access_validator(False))])
def withdraw(request: Request, body: CustomerInvestmentWithdrawReq):
    try:
        if body.amount < MIN_WITHDRAWAL:
            raise HTTPException(status_code=422, detail=f"Minimum amount withdrawable is {MIN_WITHDRAWAL}")

        requesting_user_id = request.state.user["id"]

        customer_investment = customer_investment_repo.withdraw(body.id, requesting_user_id, body.amount)
        data = CustomerInvestmentRes().dump(customer_investment)
        res = Response(data=data, code=200, message="Withdrawal successful")

        return JSONResponse(content=res.dict(), status_code=res.code)
    except HTTPException as httpexc:
        raise httpexc
