from dotenv import load_dotenv
import pytest
import sys
import os
from src.models.services.movie_service import MovieService
from src.models.services.shop_service import ShopService

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Carga las variables de entorno
load_dotenv()

# Fixtures de servicios
@pytest.fixture(scope="module")
def movie_service():
    return MovieService(base_url="http://127.0.0.1:8000")

@pytest.fixture(scope="module")
def shop_service():
    return ShopService(base_url="http://127.0.0.1:8000")

@pytest.fixture
def created_shop(shop_service):
    """Crea un shop de prueba y lo limpia después del test"""
    shop_data = {
        "address": "Test Street 123",
        "manager": "Test Manager"
    }
    response = shop_service.create_shop(shop_data=shop_data)
    shop = response.data

    if "id" not in shop:
        raise Exception(f"Error creando shop: {shop}")

    yield shop  # Entrega el shop al test

    # --- Teardown: eliminar shop después del test ---
    try:
        shop_service.delete_shop(shop["id"])
    except Exception as e:
        print(f"Error eliminando shop {shop['id']}: {e}")

@pytest.fixture
def created_movie(movie_service, created_shop):
    """Crea una película de prueba usando un shop creado"""
    movie_data = {
        "name": "Matrix",
        "director": "Wachowski",
        "genres": ["sci-fi"]
    }
    response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
    movie = response.data

    if "id" not in movie:
        raise Exception(f"Error creando película: {movie}")

    yield movie  # Entrega la película al test

    # --- Teardown: eliminar película después del test ---
    try:
        movie_service.delete_movie(movie["id"])
    except Exception as e:
        print(f"Error eliminando movie {movie['id']}: {e}")

@pytest.fixture
def sample_movie_data():
    """Datos de ejemplo para crear películas"""
    return {
        "name": "The Matrix",
        "director": "The Wachowskis",
        "genres": ["Action", "Sci-Fi"]
    }

@pytest.fixture
def sample_shop_data():
    """Datos de ejemplo para crear shops"""
    return {
        "address": "Main Street 456",
        "manager": "John Doe"
    }