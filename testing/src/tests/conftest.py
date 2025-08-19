from dotenv import load_dotenv
import pytest
import sys
import os
from services import MovieService, ShopService

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


# Carga las variables de entorno
load_dotenv()

# Fixtures de servicios
@pytest.fixture(scope="module")
def movie_service():
    return MovieService()

@pytest.fixture(scope="module")
def shop_service():
    return ShopService()

@pytest.fixture
def created_movie(movie_service):
    # Crea una película de prueba usando el servicio
    movie_data = {
        "name": "Matrix",
        "director": "Wachowski",
        "genres": ["sci-fi"],
        "shop": 1
    }
    response = movie_service.create_movie(movie_data)
    movie = response.json()  # Devuelve el dict de la película creada

    yield movie  # entrega la película al test

    # --- Teardown: eliminar película después del test ---
    movie_service.delete_movie(movie["id"])