from fastapi import APIRouter, Body, Query, Path, Depends, HTTPException
from fastapi.responses import JSONResponse
from data.schemas.core import Response, PaginatedResult
from data.schemas.investment import InvestmentReq, InvestmentRes
from server.middleware.auth import role_access_validator
from data.database import db
from data.repositories.investment import InvestmentRepository

router = APIRouter()
investment_repo = InvestmentRepository(db)

dump = InvestmentRes().dump
dump_many = InvestmentRes(many=True).dump
deps = [Depends(role_access_validator(True))]

@router.post('', dependencies=deps)
def create(body: InvestmentReq = Body(...)):
    try:
        investment = investment_repo.create(body)

        res = Response(data=dump(investment), code=201, message="Investment created")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc

@router.get('')
def get_all(page: int = Query(gt=0, default=None), per_page: int = Query(gt=0, default=None)):
    try:
        result = investment_repo.get_all(page, per_page)
        data = PaginatedResult(data=dump_many(result[1]), total=result[0], page=page, per_page=per_page) if isinstance(result, tuple) else dump_many(result)
        res = Response(data=data, code=200, message="Investments returned")
        
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc

@router.get('/{id}')
def get_one(id: int = Path(..., gt=0)):
    try:
        investment = investment_repo.get_one(id)
        
        if not investment:
            raise HTTPException(status_code=404, detail="Investment not found")

        res = Response(data=dump(investment), code=200, message="Investment returned")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc

@router.put('/{id}', dependencies=deps)
def update(id: int = Path(..., gt=0), body: InvestmentReq = Body(...)):
    try:
        body.id = id
        investment = investment_repo.update(body)

        res = Response(data=dump(investment), code=200, message="Investment updated")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc
    
@router.delete('/{id}', dependencies=deps)
def delete(id: int = Path(..., gt=0)):
    try:
        investment = investment_repo.delete(id)

        res = Response(data=True, code=200, message="Investment deleted")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as exc:
        raise exc
