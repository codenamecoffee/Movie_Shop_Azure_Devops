from pydantic import BaseModel
from typing import List
from src.models.responses.movie.movie_response import MovieResponse

class ShopResponse(BaseModel):
    id: int
    address: str
    manager: str
    movies: List[MovieResponse] = []
