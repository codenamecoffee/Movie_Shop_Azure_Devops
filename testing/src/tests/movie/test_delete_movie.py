import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response
# completed ;)
class TestDeleteMovie:

    #c8
    @pytest.mark.smoke
    def test_delete_movie_existing_id(self, movie_service, created_movie):
        response = movie_service.delete_movie(movie_id=created_movie["id"])
        assert response.status == 204

    #c11
    @pytest.mark.negative
    def test_delete_movie_nonexistent_id(self, movie_service):
        invalid_movie_id = 99999
        response = movie_service.delete_movie(movie_id=invalid_movie_id)
        assert response.status == 404

    #C20
    @pytest.mark.negative
    def test_delete_movie_non_numerical_id(self, movie_service):
        invalid_movie_id = "abc"
        response = movie_service.delete_movie(movie_id=invalid_movie_id)
        assert response.status == 422
    
    #C66
    @pytest.mark.negative
    def test_delete_shop_without_shop_id(self, shop_service):
    # Simulamos que no enviamos el id directamente
        response = shop_service.delete_shop(shop_id=None)  
        assert response.status == 422


