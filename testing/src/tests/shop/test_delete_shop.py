import os
import requests  ## Para poder automatizar "id vacío" y "sin id".
import sys
import pytest

from dotenv import load_dotenv

load_dotenv()  # Esto carga las variables del .env

BASE_URL = os.getenv("BASE_URL")

# from testing.src.tests.conftest import shop_service  // Se comentó esta línea.

# Por qué comenté la línea de arriba: (Me daba un error - ahora 45 passed y 36 warnings)
# "No necesitas importar explícitamente los fixtures desde conftest.py en tus archivos de test. 
# Pytest los detecta automáticamente si están en el mismo proyecto o subcarpeta".

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# from src.models.responses.base.response import Response 
# -> No se usa 'Response en este archivo', podemos borrar este import también.

class TestDeleteShop: 
      
    # C26 - Borra un shop empty y chequea que borró bien.
    @pytest.mark.smoke # caso correcto
    def test_delete_empty_shop_with_an_existing_shop_id(self, shop_service, created_shop):
        """C26: Eliminar un shop existente → 204"""
        response = shop_service.delete_shop(shop_id=created_shop["id"])
        assert response.status == 204

        # Opcional: verificar que el shop de prueba ya no existe
        get_response = shop_service.get_shop_by_id(created_shop["id"], response_type=dict)
        assert get_response.status == 404 # Not Found


    # C90 - Borra un shop con movies y chequea que borró también las movies.
    @pytest.mark.smoke # caso correcto
    def test_delete_shop_with_an_existing_shop_id(self, shop_service, movie_service, created_shop):
        # Creamos shop con fixtures:
        shop_id = created_shop["id"]

        # Creamos movies para agregarle:
        movie_data_1 = {"name": "movie1-test", "director": "director1-test", "genres": ["genre1"]}
        movie_data_2 = {"name": "movie2-test", "director": "director2-test", "genres": ["genre2", "genre3"]}

        movie1 = movie_service.create_movie(shop_id=shop_id, movie_data=movie_data_1).data
        movie2 = movie_service.create_movie(shop_id=shop_id, movie_data=movie_data_2).data

        # 3. Borrar el shop:
        delete_response = shop_service.delete_shop(shop_id)
        assert delete_response.status == 204 # No Content

        # 4. Verificar que las movies también fueron eliminadas:
        get_movie1 = movie_service.get_movie_by_id(movie1["id"], response_type=dict)
        get_movie2 = movie_service.get_movie_by_id(movie2["id"], response_type=dict)
        assert get_movie1.status == 404 # Not Found
        assert get_movie2.status == 404 # Not Found


    # C27
    @pytest.mark.negative # id inexistente
    def test_delete_shop_with_nonexistent_shop_id(self, shop_service):
        invalid_shop_id = 99999
        response = shop_service.delete_shop(shop_id=invalid_shop_id)
        assert response.status == 404 # Not Found

        # Chequeamos el "Appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]


    # C30
    @pytest.mark.negative # id no numérico
    def test_delete_shop_with_non_numerical_id(self, shop_service):
        non_numerical_id = "abc"
        response = shop_service.delete_shop(shop_id=non_numerical_id)
        assert response.status == 422 # Unprocessable Entity

        # Chequeamos el "Appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: int_parsing shop_id attribute." in response.data["detail"]
    

    # C31 
    @pytest.mark.negative # "id vacío"
    def test_delete_shop_with_empty_shop_id(self):
        empty_id = ""
        response = requests.delete(f"{BASE_URL}/shops/{empty_id}")
        assert response.status_code in [404, 405] # "Not Found" o "Method Not Allowed"


    # C66 
    @pytest.mark.negative # "sin id"
    def test_delete_shop_without_shop_id(self):
        response = requests.delete(f"{BASE_URL}/shops/")
        assert response.status_code in [404, 405] # "Not Found" o "Method Not Allowed"


    # C71
    @pytest.mark.negative # id negativo
    def test_delete_shop_with_negative_shop_id(self, shop_service):
        negative_shop_id = -1
        response = shop_service.delete_shop(shop_id = negative_shop_id)
        assert response.status == 404 # Not Found
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]