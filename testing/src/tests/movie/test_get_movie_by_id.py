import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response

class TestGetMovieById:
    
    #C34
    @pytest.mark.smoke
    def test_get_existing_movie_by_id_returns_correct_data(self, movie_service, created_movie):
        """TC001: Verificar que se puede obtener una película existente por ID"""
        # Arrange
        movie_id = created_movie["id"]
        
        # Act
        response = movie_service.get_movie_by_id(movie_id, response_type=dict)
        
        # Assert
        assert response.status == 200, f"Expected status 200, got {response.status}"
        
        data = response.data
        assert data["id"] == movie_id, f"Expected id {movie_id}, got {data['id']}"
        assert data["name"] == "Matrix", f"Expected name 'Matrix', got {data['name']}"
        assert data["director"] == "Wachowski", f"Expected director 'Wachowski', got {data['director']}"
        assert data["genres"] == ["sci-fi"], f"Expected genres ['sci-fi'], got {data['genres']}"
        assert "shop" in data, "Shop field is missing"
        assert data["rent"] is False, f"Expected rent False, got {data['rent']}"

    #c35 y c2
    @pytest.mark.negative
    def test_get_nonexistent_movie_by_id_returns_404(self, movie_service):
        """TC002: Verificar que obtener una película inexistente retorna 404"""
        # Arrange
        nonexistent_id = 99999
        
        # Act
        response = movie_service.get_movie_by_id(nonexistent_id, response_type=dict)
        
        # Assert
        assert response.status == 404, f"Expected status 404, got {response.status}"

    #C36
    @pytest.mark.negative
    def test_get_movie_with_empty_id(self, movie_service):
        invalid_movie_id = None  # simulamos que no se manda id
        response = movie_service.get_movie_by_id(movie_id=invalid_movie_id, response_type=dict)
        assert response.status == 422

    #C37
    @pytest.mark.negative
    def test_get_movie_with_non_numerical_id(self, movie_service):
        invalid_movie_id = "abc"  # simulamos ID no numérico
        response = movie_service.get_movie_by_id(movie_id=invalid_movie_id, response_type=dict)
        assert response.status == 422

    #C68
    @pytest.mark.negative
    def test_get_movie_without_id(self, movie_service):
        response = movie_service.get_movie_by_id(movie_id=None, response_type=dict)
        assert response.status == 422
