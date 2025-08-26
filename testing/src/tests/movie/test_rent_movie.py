import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response
# completed ;)
class TestRentMovie:
    
    # C50 
    @pytest.mark.smoke
    def test_rent_a_movie_with_an_existing_movie_id(self, movie_service, created_movie):
        movie_id = created_movie["id"]
        response = movie_service.rent_movie(movie_id=movie_id, response_type=dict)

        assert response.status == 200
        data = response.data
        assert data["id"] == movie_id
        assert data["rent"] is True


    # C52 
    @pytest.mark.negative
    def test_rent_an_already_rented_movie_with_an_existing_movie_id(self, movie_service, created_movie):
        movie_id = created_movie["id"]
        # Primero rentamos
        movie_service.rent_movie(movie_id=movie_id, response_type=dict)
        response = movie_service.rent_movie(movie_id=movie_id, response_type=dict) #intento rentar de nuevo
        assert response.status == 409


    # C51 
    @pytest.mark.negative
    def test_rent_a_movie_with_a_non_existent_movie_id(self, movie_service):
        nonexistent_id = 99999
        response = movie_service.rent_movie(movie_id=nonexistent_id, response_type=dict)
        assert response.status == 404
        