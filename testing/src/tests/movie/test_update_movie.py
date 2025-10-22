import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response

class TestUpdateMovie:  

    @pytest.mark.smoke
    def test_update_movie_with_an_existing_movie_id(self, movie_service, created_movie):
        updated_data = {
            "name": "Matrix Reloaded",
            "director": "Wachowski",
            "genres": ["Action", "Sci-Fi"]
        }
        response = movie_service.update_movie(movie_id=created_movie["id"], movie_data=updated_data)
        movie = response.data

        assert response.status == 200
        assert movie["name"] == updated_data["name"]
        assert movie["director"] == updated_data["director"]
        assert movie["genres"] == updated_data["genres"]

    @pytest.mark.negative
    def test_update_movie_with_empty_name(self, movie_service, created_movie):
        movie_data = {
            "name": "",
            "director": created_movie["director"],
            "genres": created_movie["genres"]
        }
        response = movie_service.update_movie(created_movie["id"], movie_data)
        assert response.status == 422

    @pytest.mark.negative
    def test_update_movie_with_empty_director(self, movie_service, created_movie):
        movie_data = {
            "name": created_movie["name"],
            "director": "",
            "genres": created_movie["genres"]
        }
        response = movie_service.update_movie(created_movie["id"], movie_data)
        assert response.status == 422

    @pytest.mark.negative
    def test_update_movie_with_empty_genres(self, movie_service, created_movie):
        movie_data = {
            "name": created_movie["name"],
            "director": created_movie["director"],
            "genres": []
        }
        response = movie_service.update_movie(created_movie["id"], movie_data)
        assert response.status == 422

    @pytest.mark.negative
    def test_update_movie_without_name(self, movie_service, created_movie):
        movie_data = {
            "director": created_movie["director"],
            "genres": created_movie["genres"]
        }
        response = movie_service.update_movie(created_movie["id"], movie_data)
        assert response.status == 422

    @pytest.mark.negative
    def test_update_movie_without_director(self, movie_service, created_movie):
        movie_data = {
            "name": created_movie["name"],
            "genres": created_movie["genres"]
        }
        response = movie_service.update_movie(created_movie["id"], movie_data)
        assert response.status == 422

    @pytest.mark.negative
    def test_update_movie_without_genres(self, movie_service, created_movie):
        movie_data = {
            "name": created_movie["name"],
            "director": created_movie["director"]
        }
        response = movie_service.update_movie(created_movie["id"], movie_data)
        assert response.status == 422

    @pytest.mark.negative
    def test_update_movie_with_empty_movie_id(self, movie_service, sample_movie_data):
        invalid_movie_id = None
        response = movie_service.update_movie(
            movie_id=invalid_movie_id,
            movie_data=sample_movie_data,
            response_type=dict
        )
        assert response.status == 422