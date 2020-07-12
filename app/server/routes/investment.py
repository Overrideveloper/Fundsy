from fastapi import APIRouter, Body, Query, Path, Depends, HTTPException
from fastapi.responses import JSONResponse
from data.schemas.core import Response, PaginatedResult
from data.schemas.investment import InvestmentReq, InvestmentRes
from server.middleware.auth import admin_access_validator
from data.database import db
from data.repositories.investment import InvestmentRepository

router = APIRouter()
investment_repo = InvestmentRepository(db)

dump = InvestmentRes().dump
dump_many = InvestmentRes(many=True).dump
deps = [Depends(admin_access_validator)]

@router.post('', dependencies=deps)
def create(body: InvestmentReq = Body(...)):
    try:
        investment = investment_repo.create(body)

        res = Response(data=dump(investment), code=201, message="Investment created")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as err:
        raise err

@router.get('')
def get_all(page: int = Query(alias="page", gt=0, default=None), per_page: int = Query(alias="per_page", gt=0, default=None)):
    try:
        investments = investment_repo.get_all(page, per_page)
        
        result = PaginatedResult(data=dump_many(investments), page=page, per_page=per_page) if page and per_page else dump_many(investments)

        res = Response(data=result, code=200, message="Investments returned")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as err:
        raise err

@router.get('/{id}')
def get_one(id: int = Path(..., gt=0)):
    try:
        investment = investment_repo.get_one(id)
        
        if not investment:
            raise HTTPException(status_code=404, detail="Investment not found")

        res = Response(data=dump(investment), code=200, message="Investment returned")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as err:
        raise err

@router.put('/{id}', dependencies=deps)
def update(id: int = Path(..., gt=0), body: InvestmentReq = Body(...)):
    try:
        body.id = id
        investment = investment_repo.update(body)

        res = Response(data=dump(investment), code=200, message="Investment updated")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as err:
        raise err
    
@router.delete('/{id}', dependencies=deps)
def delete(id: int = Path(..., gt=0)):
    try:
        investment = investment_repo.delete(id)

        res = Response(data=True, code=200, message="Investment deleted")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as err:
        raise err

