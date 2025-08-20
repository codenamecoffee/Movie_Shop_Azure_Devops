from dotenv import load_dotenv
import pytest
import sys
import os
from src.models.services.movie_service import MovieService
# from src.models.services.shop_service import ShopService

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


# Carga las variables de entorno
load_dotenv()

# Fixtures de servicios
@pytest.fixture(scope="module")
def movie_service():
    return MovieService(base_url="http://127.0.0.1:8000")

# @pytest.fixture(scope="module")
# def shop_service():
#     return ShopService()

@pytest.fixture
def created_movie(movie_service):
    # Crea una película de prueba usando el servicio
    movie_data = {
        "name": "Matrix",
        "director": "Wachowski",
        "genres": ["sci-fi"],
        "shop": 1
    }
    response = movie_service.create_movie(shop_id=1, movie_data=movie_data)
    # movie = response.json()  # Devuelve el dict de la película creada

    movie = response.data  # No uses response.json(), accede directamente al atributo data

    if "id" not in movie:
        raise Exception(f"Error creando película: {movie}")

    yield movie  # entrega la película al test

    # --- Teardown: eliminar película después del test ---
    movie_service.delete_movie(movie["id"])