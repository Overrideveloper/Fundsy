from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException
from .routes.customer import router as customerRouter
from .routes.auth import router as authRouter
from .routes.investment import router as investmentRouter
from .middleware.exception_handlers import http_exception_handler, validation_exception_handler
from .middleware.auth import authorization_validator
from data.seed import seed_admin

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True)

@app.exception_handler(RequestValidationError)
def _validation_exception_handler(request: Request, exc: RequestValidationError):
    return validation_exception_handler(exc)

@app.exception_handler(HTTPException)
def _http_exception_handler(request: Request, exc: HTTPException):
    return http_exception_handler(request, exc)

@app.on_event("startup")
def startup():
    seed_admin()
    print("Application is running")

app.include_router(customerRouter, prefix="/api/v1/customer", tags=["Customer"])
app.include_router(authRouter, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(investmentRouter, prefix="/api/v1/investment", tags=["Investment"], dependencies=[Depends(authorization_validator)])