import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response

class TestCreateShop:

    # C5
    @pytest.mark.smoke
    def test_create_shop(self, shop_service, sample_shop_data):
        response = shop_service.create_shop(shop_data=sample_shop_data)
        shop = response.data

        assert response.status == 201
        assert shop["address"] == sample_shop_data["address"]
        assert shop["manager"] == sample_shop_data["manager"]
        assert shop["movies"] == []


    # C6
    @pytest.mark.negative
    def test_create_shop_with_empty_address(self, shop_service, sample_shop_data):
        data = sample_shop_data.copy()
        data["address"] = ""  # lo mando empty

        response = shop_service.create_shop(shop_data=data)
    
    # valido status y mensaje
        assert response.status == 422
        assert "Address is required" in str(response.data)


    # C7 CAMPO VACIO
    @pytest.mark.negative
    def test_create_shop_with_empty_manager(self, shop_service, sample_shop_data):
        data = sample_shop_data.copy()
        data["manager"] = ""  # lo mando empty

        response = shop_service.create_shop(shop_data=data)
    
    # valido status y mensaje
        assert response.status == 422
        assert "Manager is required" in str(response.data)


    # C62 SE SACA EL CAMPO
    @pytest.mark.negative
    def test_create_shop_without_address(self, shop_service, sample_shop_data):
        data = sample_shop_data.copy()
        data.pop("address")
        response = shop_service.create_shop(shop_data=data)
        assert response.status == 422
        assert "missing address attribute" in str(response.data).lower()


    # C63
    @pytest.mark.negative
    def test_create_shop_without_manager(self, shop_service, sample_shop_data):
        data = sample_shop_data.copy()
        data.pop("manager")
        response = shop_service.create_shop(shop_data=data)
        assert response.status == 422
        assert "missing manager attribute" in str(response.data).lower()
