import os
import sys
import pytest
import requests
from dotenv import load_dotenv
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

class TestGetShopById: 

    @pytest.mark.smoke
    def test_read_shop_by_id_with_an_existing_shop_id(self, shop_service, created_shop):
        response = shop_service.get_shop_by_id(shop_id=created_shop["id"], response_type=dict)
        shop = response.data

        assert response.status == 200
        assert "id" in shop
        assert "address" in shop
        assert "manager" in shop
        assert "movies" in shop
        assert isinstance(shop["id"], int)
        assert isinstance(shop["address"], str)
        assert isinstance(shop["manager"], str)
        assert isinstance(shop["movies"], list)
        assert shop["id"] == created_shop["id"]
        assert shop["address"] == created_shop["address"]
        assert shop["manager"] == created_shop["manager"]
     
    @pytest.mark.negative
    def test_read_shop_by_id_with_a_non_existent_shop_id(self, shop_service):
        non_existent_shop_id = 99999
        response = shop_service.get_shop_by_id(shop_id=non_existent_shop_id, response_type=dict)

        assert response.status == 404
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]
 
    @pytest.mark.negative
    def test_read_shop_by_id_with_empty_shop_id(self):
        empty_id = ""
        response = requests.get(f"{BASE_URL}/shops/{empty_id}")
        assert response.status_code in [404, 405, 200]

    @pytest.mark.negative
    def test_read_shop_by_id_with_a_non_numerical_shop_id(self, shop_service):
        non_numerical_shop_id = "shop45"
        response = shop_service.get_shop_by_id(shop_id=non_numerical_shop_id, response_type=dict)

        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: int_parsing shop_id attribute." in response.data["detail"]

    @pytest.mark.negative
    def test_read_shop_by_id_without_shop_id(self):
        response = requests.get(f"{BASE_URL}/shops/")
        assert response.status_code in [404, 405, 200]

    @pytest.mark.negative
    def test_read_shop_by_id_with_a_negative_shop_id(self, shop_service):
        negative_shop_id = -1
        response = shop_service.get_shop_by_id(shop_id=negative_shop_id, response_type=dict)
        
        assert response.status == 404
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]


