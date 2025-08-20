from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Optional

from src.constants import MOVIE_NOT_FOUND_MESSAGE, SHOP_NOT_FOUND_MESSAGE, MOVIE_NOT_RENTED, MOVIE_ALREADY_RENTED
from src.schemas.schemas import Movie, MovieRequestCreate, MovieRequestUpdate, Shop, ShopRequestCreate, ShopRequestUpdate, ChangeShopRequest

# In-memory "DB"
movies: Dict[int, Movie] = {}
shops: Dict[int, Shop] = {}
_next_movie_id = 1
_next_shop_id = 1

router = APIRouter()




# Obtener Movie por name, gender y/o director (no por Shop)
@router.get("/movies/search", response_model=List[Movie], status_code=status.HTTP_200_OK)
def search_movies(
    name: Optional[str] = Query(None),
    director: Optional[str] = Query(None),
    genres: Optional[List[str]] = Query(None)
):
    # Parte de todas las movies:
    result = list(movies.values())

    # La lista de movies se irá reduciendo en función de si se ejecutan los if's o no:

    if name: # Si se especificó un nombre para filtrar.
        result = [movie for movie in result if movie.name.lower() == name.lower()]

    if director: # Si se especificó un director para filtrar.
        result = [movie for movie in result if movie.director.lower() == director.lower()]

    if genres: # Si se especificaron uno o varios géneros para filtrar.
        
        # result = [movie for movie in result  # para cada movie en result, buscar
        #           if any(movie_gender.lower() in  # si algún género (en minúscula) se encuentra en,
        #           [movie_gender.lower() for movie_gender in movie.gender] # la lista de géneros de la movie,
        #           for movie_gender in gender)] # para cada género en la lista de géneros de la movie.
        

        # Usando un for 'largo' en lugar de comprehention:
        filtered_result = []  # Para no modificar result mientras la recorremos.

        for movie in result:
          genre_list = [movie_gender.lower() for movie_gender in movie.genres]
          if all(movie_gender.lower() in genre_list for movie_gender in genres):
              filtered_result.append(movie)
              
        result = filtered_result  # Se guardan las movies que tengan TODOS los géneros especificados.

    return result



######## Crud Operations - Shops


# Obtener todos los shops
@router.get("/shops", response_model=List[Shop], status_code=status.HTTP_200_OK)
def read_all_shops():
  return list(shops.values())


# Obtener un shop por id
@router.get("/shops/{shop_id}", response_model=Shop, status_code=status.HTTP_200_OK)
def read_shop_by_id(shop_id : int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  return shops[shop_id]


# Crear shop nuevo
@router.post("/shops", response_model=Shop, status_code=status.HTTP_201_CREATED)
def create_shop(shop : ShopRequestCreate):
  global _next_shop_id
  new_shop = Shop(id = _next_shop_id, **shop.model_dump(), movies=[]) # Pusimos una lista de movies vacia para que no de error y asi no modificar el dto
  shops[_next_shop_id] = new_shop
  _next_shop_id += 1 # Actualizamos contador al final.
  return new_shop


# Actualizar shop por id
@router.put("/shops/{shop_id}", response_model=Shop, status_code=status.HTTP_200_OK)
def update_shop(shop_id : int, new_shop : ShopRequestUpdate):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])

  # Obtenemos el shop para actualizarlo:
  shop = shops[shop_id]

  # Lo actualizamos
  shop.address = new_shop.address
  shop.manager = new_shop.manager
  return shop


# Eliminar shop por id
@router.delete("/shops/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(shop_id : int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])

  id = shop_id # Variable auxiliar

  # Si el shop no está vacío:
  if shops[shop_id].movies:
    shops[shop_id].movies = [] # Eliminamos las movies.
  
  # Borramos el shop:
  _ = shops.pop(shop_id)

  # Buscamos las movies que pertenecian al shop
  movie_list = list(movies.values()) # lista auxiliar
  for movie in movie_list:
     if movie.shop == id:
      _ = movies.pop(movie.id) #Eliminamos las movies del diccionario



######## Crud Operations - Movies


# Obtener todas las movies
@router.get("/movies", response_model=List[Movie], status_code=status.HTTP_200_OK)
def read_all_movies():
  return list(movies.values())


# Obtener movie por id
@router.get("/movies/{movie_id}", response_model=Movie, status_code=status.HTTP_200_OK)
def read_movie_by_id(movie_id : int):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  return movies[movie_id]


# Crear movie
@router.post("/shops/{shop_id}/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie : MovieRequestCreate, shop_id : int):
  global _next_movie_id
  # Comprobamos que el shop exista
  if shop_id not in shops.keys():
    raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  new_movie = Movie(id=_next_movie_id, shop=shop_id, **movie.model_dump())
  movies[_next_movie_id] = new_movie
  # Agregamos la pelicula al shop especificado:
  shops[shop_id].movies.append(new_movie)
  _next_movie_id += 1 # Actualizamos contador al final.
  return new_movie


# Actualizar movie por id
@router.put("/movies/{movie_id}", response_model=Movie, status_code=status.HTTP_200_OK)
def update_movie(movie_id : int, new_movie : MovieRequestUpdate):  
  if movie_id not in movies.keys():
    raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  # Actualizamos la movie:
  movies[movie_id].name = new_movie.name
  movies[movie_id].director = new_movie.director
  movies[movie_id].genres = new_movie.genres
  # Actualizamos la movie en el shop en donde se encuentre:
  shop_id = movies[movie_id].shop
  for movie in shops[shop_id].movies:
    if movie.id == movie_id:
      movie.name = new_movie.name
      movie.director = new_movie.director
      movie.genres = new_movie.genres    
  return movies[movie_id]


# Eliminar movie
@router.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
    
    # Guardamos y borramos la movie globalmente:
    movie_to_delete = movies.pop(movie_id)

    # Borramos la movie del shop correspondiente:
    shop_id = movie_to_delete.shop
    _ = shops[shop_id].movies.remove(movie_to_delete)
    


######## Endpoints especiales


# Consultar todas las movies por Shop
@router.get("/shops/{shop_id}/movies", response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies_by_shop(shop_id: int):
   if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
   
   return shops[shop_id].movies


# Consultar todas las movies DISPONIBLES por Shop
@router.get("/shops/{shop_id}/available-movies", response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_available_movies_by_shop(shop_id: int):
   if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
   
   # Usamos list comprehention para generar una list[Movie] específica:
   return [movie for movie in shops[shop_id].movies if not movie.rent]


# Alquilar una movie: 
@router.put("/movies/{movie_id}/rent-movie", response_model=Movie, status_code=status.HTTP_200_OK)
def rent_movie(movie_id: int):
  if movie_id not in movies.keys():
    raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  if not movies[movie_id].rent:
    movies[movie_id].rent = True
    return movies[movie_id]
  raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[MOVIE_ALREADY_RENTED])


# Cambiar de shop una movie:
@router.patch("/movies/{movie_id}/change-shop", response_model=Shop, status_code=status.HTTP_200_OK) 
def change_shop_movie(movie_id: int, change_shop: ChangeShopRequest):
    
    # Obtenemos el id del shop a través del dto (No desde la URL)
    shop_id = change_shop.shop_id

    if shop_id not in shops.keys():
        raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
    if movie_id not in movies.keys():
        raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])

    movie_to_change = movies[movie_id]

    # Borramos la movie del shop donde estaba antes:
    shops[movie_to_change.shop].movies.remove(movie_to_change)

    # Cambiamos el id del shop asociado a la movie:
    movie_to_change.shop = shop_id

    # Agregamos la movie al nuevo shop:
    shops[shop_id].movies.append(movie_to_change)

    return shops[shop_id]


# Devolver una movie (Es decir, el que alquiló, la devuelve):
@router.put("/movies/{movie_id}/return-movie", response_model=Movie, status_code=status.HTTP_200_OK)
def return_movie(movie_id: int):
  if movie_id not in movies.keys():
    raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  if movies[movie_id].rent:
    movies[movie_id].rent = False
    return movies[movie_id]
  raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[MOVIE_NOT_RENTED])





