import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

class TestGetAvailableMoviesByShop:

    # C45
    @pytest.mark.smoke
    def test_get_available_movies_from_an_id_specified_shop(self, movie_service, shop_service, created_shop):
        # Creamos una movie no alquilada en el shop.
        movie_data = {"name" : "movie_prueba", "director" : "director_prueba", "genres" : ["genre1", "genre2"]}
        movie = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data).data  

        # Hacemos el GET a /shops/{shop_id}/available-movies
        response = shop_service.get_available_movies_by_shop(shop_id=created_shop["id"], response_type=dict)

        # Verificaciones
        assert response.status == 200


    # C49
    @pytest.mark.smoke
    def test_get_available_movies_from_an_id_specified_empty_shop(self, shop_service, created_shop):
        # Hacemos la consulta a la api:
        response = shop_service.get_available_movies_by_shop(shop_id=created_shop["id"], response_type=dict)

        # Verificar stats y contenido
        assert response.status == 200
        assert isinstance(response.data, list) # Se verifica que sea una lista.
        assert len(response.data) == 0  # Que esté vacía.
        

    # C86    
    @pytest.mark.smoke
    def test_get_available_movies_from_an_id_specified_shop_with_no_available_movies(self, shop_service, movie_service, created_shop):
        # Creamos las películas en el shop:
        movie_data_1 = {"name" : "movie_prueba_1", "director" : "director_prueba_1", "genres" : ["genre_prueba_1"]}
        movie_data_2 = {"name" : "movie_prueba_2", "director" : "director_prueba_2", "genres" : ["genre_prueba_2"]}

        # Manipulamos las movies como diccionarios:
        movie1 = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data_1).data
        movie2 = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data_2).data

        # Alquilamos las movies de prueba (las hacemos "no disponibles"):
        movie_service.rent_movie(movie1["id"])
        movie_service.rent_movie(movie2["id"])

        # Con estas condiciones, hacemos la consulta a la api:
        response = shop_service.get_available_movies_by_shop(shop_id=created_shop["id"], response_type=dict)

        # Verificaciones:
        assert response.status == 200
        assert isinstance(response.data, list)
        assert len(response.data) == 0  # Lista vacía porque todas las movies están alquiladas.


    # # C46    
    @pytest.mark.negative
    def test_get_available_movies_from_an_non_existent_id_specified_shop(self, shop_service):
        # shop id que no existe:
        non_existent_shop_id = 9999

        # Hacemos la consulta:
        response = shop_service.get_available_movies_by_shop(shop_id=non_existent_shop_id, response_type=dict)

        # Verificaciones:
        assert response.status == 404 # No existe el shop.

        # Chequeamos que está el "appropriate error message":
        assert "detail" in response.data  
        assert isinstance(response.data["detail"], list)  
        assert "Shop Not Found" in response.data["detail"]  


    # # C47
    @pytest.mark.negative
    def test_get_available_movies_from_a_non_numerical_id_specified_shop(self, shop_service):
        # shop id no numérico:
        non_numerical_shop_id = "invalid_id"

        # Hacemos la consulta:
        response = shop_service.get_available_movies_by_shop(shop_id=non_numerical_shop_id, response_type=dict)

        # Verificaciones:
        assert response.status == 422  # Unprocessable Entity
        
        # Chequeamos que está el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: int_parsing shop_id attribute." in response.data["detail"]
