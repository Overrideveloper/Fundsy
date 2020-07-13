from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from data.schemas.core import Response
from data.schemas.customer import CustomerRes, CustomerCreateReq
from data.repositories.customer import CustomerRepository
from data.database import db

router = APIRouter()
customer_repo = CustomerRepository(db)
dump = CustomerRes().dump

@router.post('/signup')
def signup(body: CustomerCreateReq = Body(...)):
    try:
        customer = customer_repo.signup(body)
        
        res = Response(data=dump(customer), code=201, message="Customer signed up successfully")
        return JSONResponse(content=res.dict(), status_code=res.code)
    except Exception as err:
        raise err
