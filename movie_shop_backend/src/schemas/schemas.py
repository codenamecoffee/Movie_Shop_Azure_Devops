from typing import List, Optional
from pydantic import BaseModel

# Modelo 
class Movie(BaseModel):
    id: int
    name: str
    director: str
    gender: List[str] #pasamos todos los parametros x upper desp 
    shop : int
    rent: False #booleano predeterminado false.

# DTO(s)
class MovieRequestCreate(BaseModel):
    name: str
    director: str
    gender: List[str]

class MovieRequestUpdate(BaseModel):
    name: str
    director: str
    gender: List[str]

# Modelo
class Shop(BaseModel):
    id: int
    address: str
    manager: str
    movies: List[Movie]

# DTO(s)
class ShopRequestCreate(BaseModel):
    address: str
    manager: str


class ShopRequestUpdate(BaseModel):
    address: str
    manager: str