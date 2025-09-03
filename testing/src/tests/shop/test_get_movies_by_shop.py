import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

class TestGetMoviesByShop:

    @pytest.mark.smoke
    def test_read_movies_from_shop_id_with_id_specified_shop_with_movies(self, movie_service, shop_service, created_shop):
        movie_data_1 = {"name" : "movie_prueba_1", "director" : "director_prueba_1", "genres" : ["genre_1"]}
        movie_data_2 = {"name" : "movie_prueba_2", "director" : "director_prueba_2", "genres" : ["genre_2", "genre_3"]}
        movie1 = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data_1).data
        movie2 = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data_2).data
        response = shop_service.get_movies_by_shop(shop_id=created_shop["id"], response_type=dict)
        movies_ids = [movie["id"] for movie in response.data]
        
        assert response.status == 200
        assert isinstance(response.data, list)
        assert len(response.data) >= 2
        assert movie1["id"] in movies_ids
        assert movie2["id"] in movies_ids

    @pytest.mark.smoke
    def test_read_movies_from_shop_id_with_id_specified_shop_empty(self, shop_service, created_shop):
        response = shop_service.get_movies_by_shop(shop_id=created_shop["id"], response_type=dict)
        assert response.status == 200 
        assert isinstance(response.data, list) 
        assert len(response.data) == 0

    @pytest.mark.negative
    def test_read_movies_from_shop_id_with_non_existent_shop_id(self, shop_service, created_shop):
        non_existent_shop_id = 99999
        response = shop_service.get_movies_by_shop(shop_id=non_existent_shop_id, response_type=dict)

        assert response.status == 404
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]

    @pytest.mark.negative
    def test_read_movies_from_shop_id_with_non_numerical_shop_id(self, shop_service):
        non_numerical_shop_id = "shopid23"
        response = shop_service.get_movies_by_shop(shop_id=non_numerical_shop_id, response_type=dict)

        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: int_parsing shop_id attribute." in response.data["detail"]
