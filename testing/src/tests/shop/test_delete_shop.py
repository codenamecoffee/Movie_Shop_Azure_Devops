import os
import requests
import sys
import pytest
from dotenv import load_dotenv
load_dotenv() 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

BASE_URL = os.getenv("BASE_URL")

class TestDeleteShop: 
      
    @pytest.mark.smoke 
    def test_delete_empty_shop_with_an_existing_shop_id(self, shop_service, created_shop):
        """C26: Eliminar un shop existente → 204"""
        response = shop_service.delete_shop(shop_id=created_shop["id"])
        assert response.status == 204

        get_response = shop_service.get_shop_by_id(created_shop["id"], response_type=dict)
        assert get_response.status == 404

    @pytest.mark.smoke
    def test_delete_shop_with_an_existing_shop_id(self, shop_service, movie_service, created_shop):
        shop_id = created_shop["id"]
        movie_data_1 = {"name": "movie1-test", "director": "director1-test", "genres": ["genre1"]}
        movie_data_2 = {"name": "movie2-test", "director": "director2-test", "genres": ["genre2", "genre3"]}
        movie1 = movie_service.create_movie(shop_id=shop_id, movie_data=movie_data_1).data
        movie2 = movie_service.create_movie(shop_id=shop_id, movie_data=movie_data_2).data
        delete_response = shop_service.delete_shop(shop_id)
        get_movie1 = movie_service.get_movie_by_id(movie1["id"], response_type=dict)
        get_movie2 = movie_service.get_movie_by_id(movie2["id"], response_type=dict)
        
        assert delete_response.status == 204
        assert get_movie1.status == 404
        assert get_movie2.status == 404

    @pytest.mark.negative 
    def test_delete_shop_with_nonexistent_shop_id(self, shop_service):
        invalid_shop_id = 99999
        response = shop_service.delete_shop(shop_id=invalid_shop_id)

        assert response.status == 404
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]

    @pytest.mark.negative 
    def test_delete_shop_with_non_numerical_id(self, shop_service):
        non_numerical_id = "abc"
        response = shop_service.delete_shop(shop_id=non_numerical_id)

        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: int_parsing shop_id attribute." in response.data["detail"]
    
    @pytest.mark.negative
    def test_delete_shop_with_empty_shop_id(self):
        empty_id = ""
        response = requests.delete(f"{BASE_URL}/shops/{empty_id}")
        assert response.status_code in [404, 405]

    @pytest.mark.negative
    def test_delete_shop_without_shop_id(self):
        response = requests.delete(f"{BASE_URL}/shops/")
        assert response.status_code in [404, 405]

    @pytest.mark.negative
    def test_delete_shop_with_negative_shop_id(self, shop_service):
        negative_shop_id = -1
        response = shop_service.delete_shop(shop_id = negative_shop_id)
        
        assert response.status == 404
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]