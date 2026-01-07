from pydantic import BaseModel
from typing import Any, Optional

class APIError(BaseModel):
    code: str
    message: str
    detail: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: APIError
