from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from app.data.schemas.core import Response
from typing import List, Dict

def validation_exception_handler(exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    errorCount = len(errors)
    errorList: List[Dict[str, str]] = []
    errorValues: list = []
    
    for i in range(errorCount):
        errorValue = errors[i]["loc"][len(errors[i]["loc"]) - 1]
        errorList.append({ "field": errorValue, "error": errors[i]["msg"].replace("value", errorValue) })
        errorValues.append(errorValue)
    
    msg = f"{errorCount} validation error{'s' if not errorCount or errorCount > 1 else ''} for this request: {str(errorValues)}"
    data = Response(data=errorList, code=400, message=msg)

    return JSONResponse(content=data.dict(), status_code=data.code)

def http_exception_handler(request: Request, exc: HTTPException):
    isStr = isinstance(exc.detail, str)

    data = Response(code=exc.status_code, data=None if isStr else exc.detail, message=exc.detail if isStr else "An error occurred. Please try again.")

    return JSONResponse(content=data.dict(), status_code=data.code)
