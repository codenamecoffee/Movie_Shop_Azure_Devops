from fastapi import APIRouter, HTTPException, status
from typing import List, Dict

from src.constants import MOVIE_NOT_FOUND_MESSAGE, SHOP_NOT_FOUND_MESSAGE
from src.schemas.schemas import Movie, MovieRequestCreate, MovieRequestUpdate, Shop, ShopRequestCreate, ShopRequestUpdate

# In-memory "DB"
movies: Dict[int, Movie] = {}
shops: Dict[int, Shop] = {}
_next_movie_id = 1
_next_shop_id = 1

router = APIRouter()

# Shops

# Obtener todos los shops
@router.get("/shops", response_model=List[Shop])
def read_all_shops():
  return list(shops.values())

# Obtener un shop por id
@router.get("/shops/{shop_id}", response_model=Shop)
def read_shop_by_id(shop_id : int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  return shops[shop_id]

# Crear shop nuevo
@router.post("/shop", response_model=Shop, status_code=status.HTTP_201_CREATED)
def create_shop(shop : ShopRequestCreate):
  global _next_shop_id
  new_shop = Shop(id = _next_shop_id, **shop.model_dump())
  shops[_next_shop_id] = new_shop
  _next_shop_id += 1
  return new_shop

#Updatear el shop 
@router.put("/shops/{shop_id}", response_model=Shop)
def update_shop(shop_id : int, new_shop : ShopRequestUpdate):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=422, detail=[SHOP_NOT_FOUND_MESSAGE])
  shops[shop_id].address = new_shop.address
  shops[shop_id].manager = new_shop.manager
  return shops[shop_id]

#Eliminar el shop 
@router.delete("/shops/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(shop_id : int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  _ = shops.pop(shop_id)


# Movies

#Obtener todas las movies
@router.get("/movies", response_model=List[Movie])
def read_all_movies():
  return list(shops.values())

#Obtener por id
@router.get("/movies/{movie_id}", response_model=Movie)
def read_movie_by_id(movie_id : int):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  return movies[movie_id]

#Crear movie
@router.post("/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie : MovieRequestCreate):
  global _next_movie_id
  _next_movie_id += 1
  new_movie = Movie(id=_next_movie_id, **movie.model_dump())
  movies[_next_movie_id] = new_movie
  return new_movie

#Eliminar movie
@router.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id : int):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  _ = movies.pop(movie_id)
  