import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

class TestGetMoviesByShop:

    # C29
    @pytest.mark.smoke
    def test_read_movies_from_shop_id_with_id_specified_shop_with_movies(self, movie_service, shop_service, created_shop):
        # Creamos 2 movies en el shop:
        movie_data_1 = {"name" : "movie_prueba_1", "director" : "director_prueba_1", "genres" : ["genre_1"]}
        movie_data_2 = {"name" : "movie_prueba_2", "director" : "director_prueba_2", "genres" : ["genre_2", "genre_3"]}

        # Las agregamos al shop, y las manipulamos como diccionarios:
        movie1 = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data_1).data
        movie2 = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data_2).data

        # Hacemos la consulta a la api:
        response = shop_service.get_movies_by_shop(shop_id=created_shop["id"], response_type=dict)

        # Verificaciones:
        assert response.status == 200
        assert isinstance(response.data, list) # Que se devuelva una lista.
        assert len(response.data) >= 2 # Con al menos 2 movies.

        # Verificar que las movies están en la lista del shop:
        movies_ids = [movie["id"] for movie in response.data]
        assert movie1["id"] in movies_ids
        assert movie2["id"] in movies_ids


    # C48
    @pytest.mark.smoke
    def test_read_movies_from_shop_id_with_id_specified_shop_empty(self, shop_service, created_shop):
        # Hacemos la consulta:
        response = shop_service.get_movies_by_shop(shop_id=created_shop["id"], response_type=dict)

        # Verificaciones:
        assert response.status == 200 # Ok.
        assert isinstance(response.data, list) # Se devuelve una lista.
        assert len(response.data) == 0 # Que está vacía.


    # C43
    @pytest.mark.negative
    def test_read_movies_from_shop_id_with_non_existent_shop_id(self, shop_service, created_shop):
        # shop id inexistente:
        non_existent_shop_id = 99999

        # Hacemos la consulta:
        response = shop_service.get_movies_by_shop(shop_id=non_existent_shop_id, response_type=dict)

        # Verificaciones:
        assert response.status == 404 # Not Found

        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]


    # C44
    @pytest.mark.negative
    def test_read_movies_from_shop_id_with_non_numerical_shop_id(self, shop_service):
        # shop id no numérico:
        non_numerical_shop_id = "shopid23"

        # Hacemos la consulta:
        response = shop_service.get_movies_by_shop(shop_id=non_numerical_shop_id, response_type=dict)

        # Verificaciones
        assert response.status == 422 # Unprocessable Entity

        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: int_parsing shop_id attribute." in response.data["detail"]
