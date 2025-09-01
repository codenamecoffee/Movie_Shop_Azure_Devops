import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response
class TestDeleteMovie:

    @pytest.mark.smoke
    def test_delete_movie_by_id_with_existing_movie_id(self, movie_service, created_movie):
        response = movie_service.delete_movie(movie_id=created_movie["id"])
        assert response.status == 204

    @pytest.mark.negative
    def test_delete_movie_by_id_with_non_existent_movie_id(self, movie_service):
        invalid_movie_id = 99999
        response = movie_service.delete_movie(movie_id=invalid_movie_id)
        assert response.status == 404
  
    @pytest.mark.negative
    def test_delete_movie_by_id_with_non_numerical_id(self, movie_service):
        invalid_movie_id = "abc"
        response = movie_service.delete_movie(movie_id=invalid_movie_id)
        assert response.status == 422
    



