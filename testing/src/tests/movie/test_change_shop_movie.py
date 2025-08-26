import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response
# Terminado ;)
class TestChangeShopMovie:

    # C53 
    @pytest.mark.smoke
    def test_change_a_movie_from_one_shop_to_another_id_specified_shop(self, movie_service, shop_service, created_movie, sample_shop_data):
    # Creamos un shop de destino usando sample_shop_data
        new_shop = shop_service.create_shop(shop_data=sample_shop_data).data
    # Cambiamos la movie al nuevo shop
        response = movie_service.change_shop_movie(
            movie_id=created_movie["id"],
            shop_id=new_shop["id"]
        )
        assert response.status == 200
        shop_changed = response.data
        assert shop_changed["id"] == new_shop["id"]
        assert any(m["id"] == created_movie["id"] for m in shop_changed["movies"])

    # C55 
    @pytest.mark.negative
    def test_change_a_movie_from_one_shop_to_a_non_existent_id_specified_shop(self, movie_service, created_movie):
        invalid_shop_id = 99999  # ID de shop que no existe
        response = movie_service.change_shop_movie(
            movie_id=created_movie["id"],
            shop_id=invalid_shop_id
        )
        assert response.status == 404
    
    # C54 
    @pytest.mark.negative
    def test_change_a_non_existent_movie_from_one_shop_to_another_id_specified_shop(self, movie_service, created_shop):
        invalid_movie_id = 99999  # ID de movie que no existe
        response = movie_service.change_shop_movie(
            movie_id=invalid_movie_id,
            shop_id=created_shop["id"]
        )
        assert response.status == 404
