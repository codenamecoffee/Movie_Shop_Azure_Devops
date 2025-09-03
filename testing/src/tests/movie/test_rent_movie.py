import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response
class TestRentMovie:
    
    @pytest.mark.smoke
    def test_rent_a_movie_with_an_existing_movie_id(self, movie_service, created_movie):
        movie_id = created_movie["id"]
        response = movie_service.rent_movie(movie_id=movie_id, response_type=dict)

        assert response.status == 200
        data = response.data
        assert data["id"] == movie_id
        assert data["rent"] is True
 
    @pytest.mark.negative
    def test_rent_an_already_rented_movie_with_an_existing_movie_id(self, movie_service, created_movie):
        movie_id = created_movie["id"]
        movie_service.rent_movie(movie_id=movie_id, response_type=dict)
        response = movie_service.rent_movie(movie_id=movie_id, response_type=dict) 
        assert response.status == 409
 
    @pytest.mark.negative
    def test_rent_a_movie_with_a_non_existent_movie_id(self, movie_service):
        nonexistent_id = 99999
        response = movie_service.rent_movie(movie_id=nonexistent_id, response_type=dict)
        assert response.status == 404
        