# Explicaciones del código

## main.py

En esta parte voy a dar una explicación del código en el archivo `main.py`:

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from fastapi.concurrency import asynccontextmanager

from src.constants import STATE_FILE
from src.database_manager.local_file_storage import load_state, save_state

from src.routes import api_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    api_routes.movies, api_routes.shops, api_routes._next_movie_id, api_routes._next_shop_id = load_state(STATE_FILE)
    yield
    save_state(STATE_FILE, api_routes.movies, api_routes.shops, api_routes._next_movie_id, api_routes._next_shop_id)
    
app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    if request.method == "POST" or request.method == "PUT" or request.method == "DELETE":
        save_state(STATE_FILE, api_routes.movies, api_routes.shops, api_routes._next_movie_id, api_routes._next_shop_id)
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    msgs = [ f"Validation Error: {dict_err['type']} {dict_err['loc'][1]} attribute." for dict_err in exc.errors() ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content= {"detail": msgs}
    )

app.include_router(api_routes.router)
```

Vamos parte por parte:

1. **Función `lifespan` y decorador `@asynccontextmanager`**

Existen momentos en los cuales deseamos que nuestra API Rest ejecute algunas operaciones antes del inicio o al cierre de la misma, es por esto que FastAPI permite la implementación de la función `lifespan`.

Si vemos el código dentro de la función `lifespan` cuenta de la siguiente forma:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Before yield
    yield
    # After yield
```

Acá vemos una distinción a partir de la directiva `yield`, lo que sea definido antes de `yield` será ejecutado antes de que inicie la API y lo posterior al momento en el que se apague el servicio de la API (es decir, luego de hacer Crtl+C).

Para este caso el uso de `@asynccontextmanager` es solamente una directiva para poder referir al Context Manager de Python y que se tenga un manejo asincrónico de los recursos (es algo necesario para poder trabajar con este tipo de eventos de FastAPI, pero es algo propio de Python).

Por último, es necesario definir la función `lifespan`al instanciar FastAPI de la siguiente forma:

```python
app = FastAPI(lifespan=lifespan)
```

En caso de que quieran profundizar pueden revisar [el siguiente link](https://fastapi.tiangolo.com/advanced/events/#lifespan).


Para la realidad que estamos implementando utilizamos la función `lifespan` para corroborar la existencia del archivo `app_state.json` y así cargar los datos del archivo en memoria.

2. **Decorador `@app.middleware("http")`**

En la clase se hizo mención sobre el significado de los **middleware**. Pra este caso, tenemos un middleware defido para chequear si se realizó un llamado a un POST, PUT o DELETE, lo cual se obtiene a partir del valor `request.method`. Este middleware es ejecutado siempre, por eso es necesario controlar el método HTTP utilizado a partir del siguiente if:

```python
if request.method == "POST" or request.method == "PUT" or request.method == "DELETE":
```

Posteriormente se hace un `return response` el cual es obtenido a partir de la función `response = await call_next(request)`.

Para profunddizar en el uso de middlewares dentro de FastAPI los invito a [visitar el siguiente link de la documentación de FastAPI](https://fastapi.tiangolo.com/tutorial/middleware/).

3. **Decorador `@app.exception_handler(RequestValidationError)`**

Esta función la vimos en clase y lo que hacemos es hacer una redefinición del manejo de errores genéricos de FastAPI. Para este caso en el código redefinimos el comportamiento de los errores HTTP 422 **Unprocessable Entity**.

Como se vio en la siguiente list comprehention se toman todos los valores del parámetro `exc`, la lista resultado tendrá un grupo de strings en donde se toman valores de cada elemento de la lista en `exc`: 

```python
msgs = [ f"Validation Error: {dict_err['type']} {dict_err['loc'][1]} attribute." for dict_err in exc.errors() ]
```

Por último, se pasa a armar el response creando un JSON con dos componentes, el status del request y un parámetro `details` con la lista generada anteriormente:

```python
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content= {"detail": msgs}
    )
```

## database_manager/local_file_storage.py

Dentro de este archivo vemos lo siguiente:

```python
import os, json
from typing import Dict
from src.schemas.schemas import Movie, Shop

def save_state(filename: str, movies: Dict[int, Movie], shops: Dict[int, Shop], next_movie_id: int, next_shop_id: int):
    data = {
        "movies": {k: v.model_dump() for k, v in movies.items()},
        "shops": {k: {
            "id": v.id,
            "address": v.address,
            "manager": v.manager,
            "movies": [m.id for m in v.movies]
        } for k, v in shops.items()},
        "next_movie_id": next_movie_id,
        "next_shop_id": next_shop_id
    }
    with open(filename, "w") as f:
        json.dump(data, f)

def load_state(filename: str):
    movies: Dict[int, Movie] = {}
    shops: Dict[int, Shop] = {}
    next_movie_id = 1
    next_shop_id = 1     
    if not os.path.exists(filename):
        return movies, shops, next_movie_id, next_shop_id
   
    with open(filename, "r") as f:
        data = json.load(f)
        # Load movies
        movies.clear()
        for k, v in data["movies"].items():
            movies[int(k)] = Movie(**v)
        # Load shops
        shops.clear()
        for k, v in data["shops"].items():
            shop_movies = [movies[mid] for mid in v["movies"] if mid in movies]
            shops[int(k)] = Shop(id=v["id"], address=v["address"], manager=v["manager"], movies=shop_movies)
        next_movie_id = data["next_movie_id"]
        next_shop_id = data["next_shop_id"]
    return movies, shops, next_movie_id, next_shop_id
```

1. **Función `save_state()`**

Esta función fue creada para tomar los valores dentro de cada diccionario en los que estamos guardando la información y las variables para saber el valor que se va llevando de id y así poder tener un "estado persistido de la app" dentro de un archivo en formato json.

2. **Función `load_state()`**

En complemento de la función anterior, esta función nos permite saber si el archivo existe (es decir, fue creado enel filesystem) y cargar los datos en las variables del sistema.


------
Los invito a que revisen ambas funciones y consulten por la web y luego entre nosotros si hay alguna cosa particular que no entiendan.

