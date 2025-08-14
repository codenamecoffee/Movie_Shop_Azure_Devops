from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Optional

from src.constants import MOVIE_NOT_FOUND_MESSAGE, SHOP_NOT_FOUND_MESSAGE, RESOURCE_NOT_EDITABLE
from src.schemas.schemas import Movie, MovieRequestCreate, MovieRequestUpdate, Shop, ShopRequestCreate, ShopRequestUpdate

# In-memory "DB"
movies: Dict[int, Movie] = {}
shops: Dict[int, Shop] = {}
_next_movie_id = 1
_next_shop_id = 1

router = APIRouter()


'''
    Comentarios de Teams (Nicolás):

-> Para cada Movie, NO se espera en el update que se editen los atributos rent ni shop.

-> Tanto para la edición como para la creación de un Shop, NO se espera la edición del atributo 
de lista de Movie en dicha entidad.

-> Si elimino una Movie, tengo que eliminarla dentro de la lista de Movie del Shop donde estaba.

-> Si elimino un Shop, debo eliminar todas las Movie dentro de la colección movies"

'''
######## Crud Operations - Shops


# Obtener todos los shops (CORRECTO) - Agregado status code 
@router.get("/shops", response_model=List[Shop], status_code=status.HTTP_200_OK)
def read_all_shops():
  return list(shops.values())


# Obtener un shop por id (CORRECTO) - Agregado status code
@router.get("/shops/{shop_id}", response_model=Shop, status_code=status.HTTP_200_OK)
def read_shop_by_id(shop_id : int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  return shops[shop_id]


# Crear shop nuevo (CORRECTO)
@router.post("/shop", response_model=Shop, status_code=status.HTTP_201_CREATED)
def create_shop(shop : ShopRequestCreate):
  global _next_shop_id
  new_shop = Shop(id = _next_shop_id, **shop.model_dump(), movies=[]) # Pusimos una lista de movies vacia para que no de error y asi no modificar el dto
  shops[_next_shop_id] = new_shop
  _next_shop_id += 1 # Actualizamos contador al final.
  return new_shop


# Actualizar shop por id (CORRECTO) - Actualizado el status code
@router.put("/shops/{shop_id}", response_model=Shop, status_code=status.HTTP_200_OK)
def update_shop(shop_id : int, new_shop : ShopRequestUpdate):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  # Actualizamos el shop:
  shops[shop_id].address = new_shop.address
  shops[shop_id].manager = new_shop.manager
  return shops[shop_id]


# Eliminar shop por id (CORRECTO) - Actualizado
@router.delete("/shops/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shop(shop_id : int):
  if shop_id not in shops.keys():
      raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
  # Si el shop no está vacío:
  if shops[shop_id].movies:
    shops[shop_id].movies = [] # Eliminamos las movies.
  # Borramos el shop:
  _ = shops.pop(shop_id)



######## Crud Operations - Movies


# Obtener todas las movies (CORRECTO)
@router.get("/movies", response_model=List[Movie], status_code=status.HTTP_200_OK)
def read_all_movies():
  return list(movies.values())


#Obtener movie por id (CORRECTO)
@router.get("/movies/{movie_id}", response_model=Movie, status_code=status.HTTP_200_OK)
def read_movie_by_id(movie_id : int):
  if movie_id not in movies.keys():
      raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  return movies[movie_id]


# Crear movie (CORRECTO) - Actualizado: (Ubicación de la línea: next_movie_id += 1 / Chequear si existe el shop)
@router.post("/shop/{shop_id}/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
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


# Actualizar movie por id (CORRECTO) - Hecho nuevo
@router.put("/movie/{movie_id}", response_model=Movie, status_code=status.HTTP_200_OK)
def update_movie(movie_id : int, new_movie : MovieRequestUpdate):  
  if movie_id not in movies.keys():
    raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  # Actualizamos la movie:
  movies[movie_id].name = new_movie.name
  movies[movie_id].director = new_movie.director
  movies[movie_id].gender = new_movie.gender
  # Actualizamos la movie en el shop en donde se encuentre:
  shops[movies[movie_id].shop].movies[movie_id].name = new_movie.name
  shops[movies[movie_id].shop].movies[movie_id].director = new_movie.director
  shops[movies[movie_id].shop].movies[movie_id].gender = new_movie.gender
  return movies[movie_id]



#Eliminar movie (CORRECTO)
@router.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
    
    # Guardamos y borramos la movie globalmente
    movie_to_delete = movies.pop(movie_id)

    # Borramos la movie del shop correspondiente
    shop_id = movie_to_delete.shop
    _ = shops[shop_id].movies.pop(movie_id)
    

######## Endpoints especiales (Pendientes)


# Alquilar una movie:
@router.put("/movies/{movie_id}", response_model=Movie ,status_code=status.HTTP_200_OK)
def rent_movie(movie_id: int):
  if movie_id not in movies.keys():
    raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  if not movies[movie_id].rent:
    movies[movie_id].rent = True
    return movies[movie_id]
  raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[RESOURCE_NOT_EDITABLE])

# Cambiar de shop una movie:
@router.put("/shop/{shop_id}/movies/{movie_id}", response_model=Shop, status_code=status.HTTP_200_OK)
def change_shop_movie(shop_id: int, movie_id: int):
    if shop_id not in shops:
        raise HTTPException(status_code=404, detail=[SHOP_NOT_FOUND_MESSAGE])
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])

    movie_to_change = movies[movie_id]

    # Borramos la movie del shop donde estaba antes
    shops[movie_to_change.shop].movies.remove(movie_to_change)

    # Cambiamos el id del shop asociado a la movie
    movie_to_change.shop = shop_id

    # Agregamos la movie al nuevo shop
    shops[shop_id].movies.append(movie_to_change)

    return shops[shop_id]


# Devolver una movie (Es decir, el que alquiló, la devuelve):
@router.put("/movies/{movie_id}", response_model=Movie, status_code=status.HTTP_200_OK)
def return_movie(movie_id: int):
  if movie_id not in movies.keys():
    raise HTTPException(status_code=404, detail=[MOVIE_NOT_FOUND_MESSAGE])
  if movies[movie_id].rent:
    movies[movie_id].rent = False
    return movies[movie_id]
  raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[RESOURCE_NOT_EDITABLE])


# Obtener Movie por name, gender y/o director (no por Shop)
@router.get("/movies/search", response_model=List[Movie], status_code=status.HTTP_200_OK)
# def search_movie(
#     name: Optional[str] = None, 
#     gender: Optional[List[str]] = Query(None), 
#     director: Optional[str] = None
# ):
          
#     results = list(movies.values())

#     if name:
#       results = [m for m in results if name.lower() in m["name"].lower()]

# # Filtramos por director si se pasó
#     if director:
#       results = [m for m in results if director.lower() in m["director"].lower()]

# # Filtramos por géneros si se pasó
#     if gender:
#       results = [m for m in results if any(g.lower() in [x.lower() for x in m["gender"]] for g in gender)]
    
#     return results


def search_movies(
    name: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    director: Optional[str] = Query(None)
):
    movies = get_movies()  # Trae todas las películas de la base de datos
    # Filtra según los parámetros recibidos
    if name:
        movies = [m for m in movies if m.name.lower() == name.lower()]
    if genre:
        movies = [m for m in movies if m.genre.lower() == genre.lower()]
    if director:
        movies = [m for m in movies if m.director.lower() == director.lower()]
    return movies              

#GET /movies?name=casablanca&director=..&gender=romatico&gender=action&gender=.. 

