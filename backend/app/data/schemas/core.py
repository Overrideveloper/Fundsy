from pydantic.generics import GenericModel
from pydantic import BaseModel, Field
from typing import Any, Optional, List

class Response(BaseModel):
    data: Optional[Any]
    code: int
    message: str

class PaginatedResult(BaseModel):
    data: List[Any]
    total: int
    page: int
    per_page: int
