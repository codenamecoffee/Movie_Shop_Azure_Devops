from pydantic import BaseModel
from typing import List


class ErrorResponse(BaseModel):
    detail: List[str]
