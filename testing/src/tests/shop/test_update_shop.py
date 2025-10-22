import os
import requests
import sys
import pytest
from dotenv import load_dotenv, find_dotenv
from src.models.requests.shop.add_shop_model import AddShopModel

env_file = find_dotenv()
if not env_file:
    if os.path.exists("/app/testing/.env"):
        env_file = "/app/testing/.env"
    else:
        env_file = os.path.join(os.path.dirname(__file__), "../../.env")

load_dotenv(env_file, override=True)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

BASE_URL = os.getenv("BASE_URL")



class TestUpdateShop:

    @pytest.mark.smoke
    def test_update_shop_with_an_existing_shop_id(self, shop_service, created_shop):
        updated_shop_model = AddShopModel(
            address="Nueva Dirección 1",
            manager="Nuevo Manager 1"
        )
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop=updated_shop_model,
            response_type=dict
        )
        updated_shop = response.data

        assert response.status == 200
        assert "id" in updated_shop
        assert "address" in updated_shop
        assert "manager" in updated_shop
        assert "movies" in updated_shop

        assert isinstance(updated_shop["id"], int)
        assert isinstance(updated_shop["address"], str)
        assert isinstance(updated_shop["manager"], str)
        assert isinstance(updated_shop["movies"], list)

        assert updated_shop["id"] == created_shop["id"]
        assert updated_shop["address"] == updated_shop_model.address
        assert updated_shop["manager"] == updated_shop_model.manager
        assert updated_shop["movies"] == created_shop["movies"]

    @pytest.mark.negative
    def test_update_shop_with_non_existent_shop_id(self, shop_service):
        non_existent_shop_id = 99999
        updated_shop_model = AddShopModel(
            address="Dirección Inexistente",
            manager="Manager Inexistente"
        )
        response = shop_service.update_shop(
            shop_id=non_existent_shop_id,
            shop=updated_shop_model,
            response_type=dict
        )

        assert response.status == 404
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_with_empty_shop_id(self):
        empty_id = ""
        updated_shop_model = AddShopModel(
            address="Nueva Dirección",
            manager="Nuevo Manager"
        )
        response = requests.put(
            f"{BASE_URL}/shops/{empty_id}", 
            json=updated_shop_model.__dict__ 
        )
        error_data = response.json()

        assert response.status_code == 405
        assert "detail" in error_data
        assert isinstance(error_data["detail"], str)
        assert "Method Not Allowed" in error_data["detail"]

    @pytest.mark.negative
    def test_update_shop_with_non_numerical_shop_id(self, shop_service):
        non_numerical_shop_id = "shop123"
        updated_shop_model = AddShopModel(
            address="Nueva Dirección",
            manager="Nuevo Manager"
        )

        response = shop_service.update_shop(
            shop_id=non_numerical_shop_id,
            shop=updated_shop_model, 
            response_type=dict
        )
    
        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert any("int_parsing shop_id" in msg for msg in response.data["detail"])

    @pytest.mark.negative
    def test_update_shop_with_negative_shop_id(self, shop_service):
        negative_shop_id = -1
        updated_shop_model = AddShopModel(
            address="Nueva Dirección",
            manager="Nuevo Manager"
        )

        response = shop_service.update_shop(
            shop_id=negative_shop_id,
            shop=updated_shop_model, 
            response_type=dict
        )
    
        assert response.status == 404
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert any("Shop Not Found" in msg for msg in response.data["detail"])

    @pytest.mark.negative
    def test_update_shop_with_required_attributes_empty(self, shop_service, created_shop):
        updated_shop_dict = {"address": "", "manager": ""}

        try:
            updated_shop_model = AddShopModel(**updated_shop_dict)
            response = shop_service.update_shop(
                shop_id=created_shop["id"],
                shop=updated_shop_model,
                response_type=dict
            )
        except Exception as e:
            response = e  
        assert isinstance(response, Exception) or (response.status == 422)

    @pytest.mark.smoke
    def test_update_shop_with_new_address(self, shop_service, created_shop):
        updated_shop_model = AddShopModel(
            address="Nueva Dirección Solo Address",
            manager=created_shop["manager"]
        )

        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop=updated_shop_model, 
            response_type=dict
        )
        updated_shop = response.data

        assert response.status == 200
        assert "id" in updated_shop
        assert "address" in updated_shop
        assert "manager" in updated_shop
        assert "movies" in updated_shop

        assert isinstance(updated_shop["id"], int)
        assert isinstance(updated_shop["address"], str)
        assert isinstance(updated_shop["manager"], str)
        assert isinstance(updated_shop["movies"], list)

        assert updated_shop["id"] == created_shop["id"]
        assert updated_shop["address"] == updated_shop_model.address
        assert updated_shop["manager"] == updated_shop_model.manager
        assert updated_shop["movies"] == created_shop["movies"]

    @pytest.mark.smoke
    def test_update_shop_with_new_manager(self, shop_service, created_shop):
        updated_shop_model = AddShopModel(
            address=created_shop["address"],
            manager="Manager nuevo"
        )

        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop=updated_shop_model, 
            response_type=dict
        )
        updated_shop = response.data

        assert response.status == 200
        assert "id" in updated_shop
        assert "address" in updated_shop
        assert "manager" in updated_shop
        assert "movies" in updated_shop

        assert isinstance(updated_shop["id"], int)
        assert isinstance(updated_shop["address"], str)
        assert isinstance(updated_shop["manager"], str)
        assert isinstance(updated_shop["movies"], list)

        assert updated_shop["id"] == created_shop["id"]
        assert updated_shop["address"] == updated_shop_model.address
        assert updated_shop["manager"] == updated_shop_model.manager
        assert updated_shop["movies"] == created_shop["movies"]

    @pytest.mark.negative
    def test_update_shop_with_empty_address(self, shop_service, created_shop):
        updated_shop_model = AddShopModel(
            address="",
            manager="Manager Válido"
        )
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop=updated_shop_model,
            response_type=dict
        )
        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Address is required" in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_with_empty_manager(self, shop_service, created_shop):
        updated_shop_model = AddShopModel(
            address=created_shop["address"],
            manager=""
        )
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop=updated_shop_model,
            response_type=dict
        )

        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Manager is required" in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_without_address(self, shop_service, created_shop):
        updated_shop_model = AddShopModel(address="", manager="Manager Válido")

        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop=updated_shop_model,
            response_type=dict
        )

        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Address is required" in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_without_manager(self, shop_service, created_shop):
        updated_shop_model = AddShopModel(address="Address válido", manager="")

        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop=updated_shop_model,
            response_type=dict
        )

        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Manager is required" in response.data["detail"]

    