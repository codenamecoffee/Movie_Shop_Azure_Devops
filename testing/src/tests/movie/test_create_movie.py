import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
class TestCreateMovie:

    @pytest.mark.smoke
    def test_create_a_movie_with_an_existing_shop_id(self, movie_service, created_shop, sample_movie_data):
        movie_data = sample_movie_data.copy()
        movie_data["genres"] = ["Action", "Sci-Fi"] 
        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        movie = response.data

        assert response.status == 201
        assert movie["name"] == movie_data["name"]
        assert movie["director"] == movie_data["director"]
        assert movie["genres"] == movie_data["genres"]
        assert movie["shop"] == created_shop["id"]

   
    @pytest.mark.negative
    def test_create_movie_with_empty_name(self, movie_service, created_shop, sample_movie_data):
        """Intentar crear película sin name → debe retornar 422"""
        movie_data = sample_movie_data.copy()
        movie_data["name"] = "" 

        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422  
 
    @pytest.mark.negative
    def test_create_movie_with_empty_director(self, movie_service, created_shop, sample_movie_data):
        movie_data = sample_movie_data.copy()
        movie_data["director"] = "" 

        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422 

    @pytest.mark.negative
    def test_create_movie_with_empty_genres(self, movie_service, created_shop, sample_movie_data):
        movie_data = sample_movie_data.copy()
        movie_data["genres"] = []  

        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422  
  
    @pytest.mark.negative
    def test_create_a_movie_with_non_existent_shop_id(self, movie_service, sample_movie_data):
        invalid_shop_id = 99999
        response = movie_service.create_movie(shop_id=invalid_shop_id, movie_data=sample_movie_data)
        assert response.status in [404]

    @pytest.mark.negative
    def test_create_movie_without_director(self, movie_service, created_shop, sample_movie_data):
        movie_data = sample_movie_data.copy()
        movie_data.pop("director")  
        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422

    @pytest.mark.negative
    def test_create_movie_without_name(self, movie_service, created_shop, sample_movie_data):
        movie_data = sample_movie_data.copy()
        movie_data.pop("name") 
        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422

    @pytest.mark.negative
    def test_create_movie_without_genres(self, movie_service, created_shop, sample_movie_data):
        movie_data = sample_movie_data.copy()
        movie_data.pop("genres") 
        response = movie_service.create_movie(shop_id=created_shop["id"], movie_data=movie_data)
        assert response.status == 422

    @pytest.mark.negative
    def test_create_a_movie_with_non_numerical_shop_id(self, movie_service, sample_movie_data):
        invalid_shop_id = "abc"
        response = movie_service.create_movie(shop_id=invalid_shop_id, movie_data=sample_movie_data)
        assert response.status in [422]

    @pytest.mark.negative
    def test_create_movie_with_empty_shop_id(self, movie_service, sample_movie_data):
        invalid_shop_id = ""
        response = movie_service.create_movie(shop_id=invalid_shop_id, movie_data=sample_movie_data)
        assert response.status == 404

    @pytest.mark.negative
    def test_create_movie_without_shop_id(self, movie_service, sample_movie_data):
        response = movie_service.create_movie(shop_id=None, movie_data=sample_movie_data)
        assert response.status == 422

