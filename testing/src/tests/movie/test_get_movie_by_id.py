import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response

class TestGetMovieById:  # Faltan: C32, C33 (Son de Read All Movies) y C72
    
    # C34 
    @pytest.mark.smoke
    def test_read_movie_by_id_with_existing_movie_id(self, movie_service, created_movie):
        # Creamos una movie y obtenemos su id:
        movie_id = created_movie["id"]
        
        # Hacemos la consulta con ese id:
        response = movie_service.get_movie_by_id(movie_id, response_type=dict)
        
        # Validaciones:
        assert response.status == 200, f"Expected status 200, got {response.status}"
        
        # Validación de la estructura de la movie:
        data = response.data
        assert data["id"] == movie_id, f"Expected id {movie_id}, got {data['id']}"
        assert data["name"] == "Matrix", f"Expected name 'Matrix', got {data['name']}"
        assert data["director"] == "Wachowski", f"Expected director 'Wachowski', got {data['director']}"
        assert data["genres"] == ["sci-fi"], f"Expected genres ['sci-fi'], got {data['genres']}"
        assert "shop" in data, "Shop field is missing"
        assert data["rent"] is False, f"Expected rent False, got {data['rent']}"


    # C35  
    @pytest.mark.negative
    def test_read_movie_by_id_with_non_existent_movie_id(self, movie_service):
        # id inexistente:
        non_existent_id = 99999
        
        # Hacemos la consulta:
        response = movie_service.get_movie_by_id(non_existent_id, response_type=dict)
        
        # Validaciones:
        assert response.status == 404, f"Expected status 404, got {response.status}"


    # C36 
    @pytest.mark.negative
    def test_read_movie_by_id_with_empty_movie_id(self, movie_service):
        invalid_movie_id = None  # simulamos que no se manda id
        response = movie_service.get_movie_by_id(movie_id=invalid_movie_id, response_type=dict)
        assert response.status == 422


    # C37  
    @pytest.mark.negative
    def test_read_movie_by_id_with_non_numerical_movie_id(self, movie_service):
        invalid_movie_id = "abc"  # simulamos ID no numérico
        response = movie_service.get_movie_by_id(movie_id=invalid_movie_id, response_type=dict)
        assert response.status == 422


    # C68 
    @pytest.mark.negative
    def test_read_movie_by_id_without_movie_id(self, movie_service):
        response = movie_service.get_movie_by_id(movie_id=None, response_type=dict)
        assert response.status == 422

