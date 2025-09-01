from pydantic import BaseModel
from typing import List

class MovieResponse(BaseModel):
    id: int
    name: str
    director: str
    genres: List[str]
    shop: int
    rent: bool

