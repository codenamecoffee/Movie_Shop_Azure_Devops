import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response
#terminado ;)
class TestCreateMovie:

    # C15 
    @pytest.mark.smoke
    def test_create_a_movie_with_an_existing_shop_id(self, movie_service, created_shop, sample_movie_data):
        #Crear película con shop existente y múltiples géneros
        movie_data = sample_movie_data.copy()
        movie_data["genres"] = ["Action", "Sci-Fi"] #buscar
        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        movie = response.data

        assert response.status == 201
        assert movie["name"] == movie_data["name"]
        assert movie["director"] == movie_data["director"]
        assert movie["genres"] == movie_data["genres"]
        assert movie["shop"] == created_shop["id"]

    #casos negativos
    # C79 
    @pytest.mark.negative
    def test_create_movie_with_empty_name(self, movie_service, created_shop, sample_movie_data):
        """Intentar crear película sin name → debe retornar 422"""
        movie_data = sample_movie_data.copy()
        movie_data["name"] = ""  # lo mando empty

        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422  # lanza el status

    # C78 
    @pytest.mark.negative
    def test_create_movie_with_empty_director(self, movie_service, created_shop, sample_movie_data):
        movie_data = sample_movie_data.copy()
        movie_data["director"] = ""  # lo mando empty

        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422  # lanza el status

    # C77
    @pytest.mark.negative
    def test_create_movie_with_empty_genres(self, movie_service, created_shop, sample_movie_data):
        movie_data = sample_movie_data.copy()
        movie_data["genres"] = []  # vacía

        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422  # lanza el status

    # C19  
    @pytest.mark.negative
    def test_create_a_movie_with_non_existent_shop_id(self, movie_service, sample_movie_data):
        #Crear película con shop inexistente
        invalid_shop_id = 99999
        response = movie_service.create_movie(shop_id=invalid_shop_id, movie_data=sample_movie_data)
        assert response.status in [404]

    # C74
    @pytest.mark.negative
    def test_create_movie_without_director(self, movie_service, created_shop, sample_movie_data):
     #eliminamos el campo
        movie_data = sample_movie_data.copy()
        movie_data.pop("director")  # lo sacamos directamente, implementamos el pop en vez de crear todos los campos de a uno y sacar ese
        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422

    # C73
    @pytest.mark.negative
    def test_create_movie_without_name(self, movie_service, created_shop, sample_movie_data):
     #eliminamos el campo
        movie_data = sample_movie_data.copy()
        movie_data.pop("name")  # lo sacamos directamente
        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422

    # C75
    @pytest.mark.negative
    def test_create_movie_without_genres(self, movie_service, created_shop, sample_movie_data):
     #eliminamos el campo
        movie_data = sample_movie_data.copy()
        movie_data.pop("genres")  # lo sacamos directamente
        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422

    # C25 
    @pytest.mark.negative
    def test_create_a_movie_with_non_numerical_shop_id(self, movie_service, sample_movie_data):
        #Crear película con shop no numérico
        invalid_shop_id = "abc"
        response = movie_service.create_movie(shop_id=invalid_shop_id, movie_data=sample_movie_data)
        assert response.status in [422]

    # C80
    @pytest.mark.negative
    def test_create_movie_with_empty_shop_id(self, movie_service, sample_movie_data):
        invalid_shop_id = ""
        response = movie_service.create_movie(shop_id=invalid_shop_id, movie_data=sample_movie_data)
        assert response.status == 404

    # C81
    @pytest.mark.negative
    def test_create_movie_without_shop_id(self, movie_service, sample_movie_data):
        #Crea movie sin pasar shop_id, simulando que no se manda
        # Ponemos None para simular que no se manda el shop_id
        response = movie_service.create_movie(shop_id=None, movie_data=sample_movie_data)
        assert response.status == 422

