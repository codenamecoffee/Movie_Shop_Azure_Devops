import os
import sys
import pytest
import requests
from dotenv import load_dotenv
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

class TestUpdateShop:

    @pytest.mark.smoke
    def test_update_shop_with_an_existing_shop_id(self, shop_service, created_shop):
        updated_shop_data = {
            "address" : "Nueva Dirección 1",
            "manager" : "Nuevo Manager 1"
        }
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
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
        assert updated_shop["address"] == updated_shop_data["address"]
        assert updated_shop["manager"] == updated_shop_data["manager"]
        assert updated_shop["movies"] == created_shop["movies"]

    @pytest.mark.negative
    def test_update_shop_with_non_existent_shop_id(self, shop_service):
        non_existent_shop_id = 99999
        updated_shop_data = {
            "address": "Dirección Inexistente",
            "manager": "Manager Inexistente"
        }
        response = shop_service.update_shop(
            shop_id=non_existent_shop_id,
            shop_data=updated_shop_data,
            response_type=dict
        )
    
        assert response.status == 404
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_with_empty_shop_id(self):
        empty_id = ""
        updated_shop_data = {
            "address": "Nueva Dirección",
            "manager": "Nuevo Manager"
        }
        response = requests.put(f"{BASE_URL}/shops/{empty_id}", json=updated_shop_data)
        error_data = response.json()

        assert response.status_code == 405
        assert "detail" in error_data
        assert isinstance(error_data["detail"], str)
        assert "Method Not Allowed" in error_data["detail"]

    @pytest.mark.negative
    def test_update_shop_with_non_numerical_shop_id(self, shop_service):
        non_numerical_shop_id = "shop123"
        updated_shop_data = {
            "address": "Nueva Dirección",
            "manager": "Nuevo Manager"
        }
        response = shop_service.update_shop(
            shop_id=non_numerical_shop_id,
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: int_parsing shop_id attribute." in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_with_negative_shop_id(self, shop_service):
        negative_shop_id = -1
        updated_shop_data = {
            "address": "Nueva Dirección",
            "manager": "Nuevo Manager"
        }
        response = shop_service.update_shop(
            shop_id=negative_shop_id,
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        assert response.status == 404
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_with_required_attributes_empty(self, shop_service, created_shop):
        updated_shop_data_with_empty_required_attributes = {
            "address": "", 
            "manager": ""   
        }
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data_with_empty_required_attributes,
            response_type=dict
        )
        detail_messages = response.data["detail"]

        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Address is required" in detail_messages or "Manager is required" in detail_messages
       
    @pytest.mark.smoke
    def test_update_shop_with_new_address(self, shop_service, created_shop):
        updated_shop_data = {
            "address": "Nueva Dirección Solo Address",
            "manager": created_shop["manager"]
        }
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
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
        assert updated_shop["address"] == updated_shop_data["address"] 
        assert updated_shop["manager"] == created_shop["manager"] 
        assert updated_shop["movies"] == created_shop["movies"]  

    @pytest.mark.smoke
    def test_update_shop_with_new_manager(self, shop_service, created_shop):
        updated_shop_data = {
            "address": created_shop["address"], 
            "manager": "Manager nuevo" 
        }
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
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
        assert updated_shop["address"] == created_shop["address"] 
        assert updated_shop["manager"] == updated_shop_data["manager"]
        assert updated_shop["movies"] == created_shop["movies"]

    @pytest.mark.negative
    def test_update_shop_with_empty_address(self, shop_service, created_shop):
        updated_shop_data = {
            "address": "",  
            "manager": "Manager Válido" 
        }
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Address is required" in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_with_empty_manager(self, shop_service, created_shop):
        updated_shop_data = {
            "address": "address válido",
            "manager": ""
        }
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Manager is required" in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_without_address(self, shop_service, created_shop):
        updated_shop_data = {
            "manager": "Manager Válido"
        }
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: missing address attribute." in response.data["detail"]

    @pytest.mark.negative
    def test_update_shop_without_manager(self, shop_service, created_shop):
        updated_shop_data = {
            "address" : "address válido" 
        }
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        assert response.status == 422
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: missing manager attribute." in response.data["detail"]

    