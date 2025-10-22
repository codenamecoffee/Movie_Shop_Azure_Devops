import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.requests.shop.add_shop_model import AddShopModel
from src.models.responses.shop.shop_response import ShopResponse


class TestCreateShop:

    @pytest.mark.smoke
    def test_create_shop(self, shop_service, sample_shop_data):
        shop_model = AddShopModel(**sample_shop_data) 
        response = shop_service.create_shop(shop=shop_model, response_type=ShopResponse)
        shop = response.data

        assert response.status == 201
        assert shop.address == sample_shop_data["address"]
        assert shop.manager == sample_shop_data["manager"]
        assert shop.movies == []
   
    @pytest.mark.negative
    def test_create_shop_with_empty_address(self, shop_service, sample_shop_data):
        data = sample_shop_data.copy()
        data["address"] = ""
        shop_model = AddShopModel(**data)
        response = shop_service.create_shop(shop=shop_model, response_type=ShopResponse)
    
        assert response.status == 422
        assert "Address is required" in str(response.data)
        
    @pytest.mark.negative
    def test_create_shop_with_empty_manager(self, shop_service, sample_shop_data):
        data = sample_shop_data.copy()
        data["manager"] = ""
        shop_model = AddShopModel(**data)
        response = shop_service.create_shop(shop=shop_model, response_type=ShopResponse)
    
        assert response.status == 422
        assert "Manager is required" in str(response.data)

    @pytest.mark.negative
    def test_create_shop_without_address(self, shop_service, sample_shop_data):
        data = sample_shop_data.copy()
        data.pop("address")
        try:
            shop_model = AddShopModel(**data)
            response = shop_service.create_shop(shop=shop_model, response_type=ShopResponse)
            assert response.status == 422
        except (TypeError, ValueError):  
            pass


    @pytest.mark.negative
    def test_create_shop_without_manager(self, shop_service, sample_shop_data):
        data = sample_shop_data.copy()
        data.pop("manager")
        try:
            shop_model = AddShopModel(**data)
            response = shop_service.create_shop(shop=shop_model, response_type=ShopResponse)
            assert response.status == 422
        except (TypeError, ValueError):
            pass    