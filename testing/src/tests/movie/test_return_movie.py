import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response
# completed ;)
class TestReturnMovie:

    # C56 Devolver una movie que está alquilada
    @pytest.mark.smoke
    def test_return_existing_rented_movie(self, movie_service, created_movie):
        #Primero alquilamos la movie para poder devolverla
        movie_service.rent_movie(movie_id=created_movie["id"], response_type=dict)
        #devolvemos la movie
        response = movie_service.return_movie(movie_id=created_movie["id"], response_type=dict)
        assert response.status == 200
        data = response.data
        assert data["id"] == created_movie["id"]
        assert data["rent"] is False

    # C57
    @pytest.mark.negative
    def test_return_already_returned_movie(self, movie_service, created_movie):
        #nos fijamos que este devuelta
        movie_service.return_movie(movie_id=created_movie["id"], response_type=dict)
        response = movie_service.return_movie(movie_id=created_movie["id"], response_type=dict)
        assert response.status == 409 

    # C58
    @pytest.mark.negative
    def test_return_nonexistent_movie(self, movie_service):
        nonexistent_id = 99999
        response = movie_service.return_movie(movie_id=nonexistent_id, response_type=dict)
        assert response.status == 404