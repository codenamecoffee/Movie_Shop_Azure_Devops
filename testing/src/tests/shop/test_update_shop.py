import os
import sys
import pytest
import requests  ## Para poder automatizar "id vacío" y "sin id".

from dotenv import load_dotenv
load_dotenv()  # Esto carga las variables del .env
BASE_URL = os.getenv("BASE_URL")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


class TestUpdateShop:

    # C14
    @pytest.mark.smoke
    def test_update_shop_with_an_existing_shop_id(self, shop_service, created_shop):
        # Datos para actualizar el shop:
        updated_shop_data = {
            "address" : "Nueva Dirección 1",
            "manager" : "Nuevo Manager 1"
            # Nota: "movies" no se incluye porque no es modificable via PUT /shops/{id}

        }

        # Hacemos la consulta a la api (update):
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )

        # Verificaciones:
        assert response.status == 200 # Ok

        # Verificamos estructura válida del shop actualizado:
        updated_shop = response.data # Para poder manipularlo mejor.

        assert "id" in updated_shop # Si posee el atributo id.
        assert "address" in updated_shop # Si posee el atributo address.
        assert "manager" in updated_shop # Si posee el atributo manager.
        assert "movies" in updated_shop # Si posee el atributo movies.

        # Verificamos tipos de datos de los atributos:
        assert isinstance(updated_shop["id"], int)
        assert isinstance(updated_shop["address"], str)
        assert isinstance(updated_shop["manager"], str)
        assert isinstance(updated_shop["movies"], list)
    
        # Verificamos que los datos se actualizaron correctamente:
        assert updated_shop["id"] == created_shop["id"]  # id no cambia.
        assert updated_shop["address"] == updated_shop_data["address"]  # Nuevo valor.
        assert updated_shop["manager"] == updated_shop_data["manager"]  # Nuevo valor.
        assert updated_shop["movies"] == created_shop["movies"]  # Lista de movies NO cambia.


    # C18
    @pytest.mark.negative
    def test_update_shop_with_non_existent_shop_id(self, shop_service):
        # shop id que no existe:
        non_existent_shop_id = 99999
        
        # Datos válidos para actualizar (aunque el shop no existe):
        updated_shop_data = {
            "address": "Dirección Inexistente",
            "manager": "Manager Inexistente"
        }
        
        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=non_existent_shop_id,
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 404  # Not Found
        
        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]



    # C22 - "id vacío"   
    @pytest.mark.negative
    def test_update_shop_with_empty_shop_id(self):
         # shop id vacío:
        empty_id = ""
        
        # Datos válidos para actualizar:
        updated_shop_data = {
            "address": "Nueva Dirección",
            "manager": "Nuevo Manager"
        }
        
        # Hacemos la consulta PUT con "id vacío":
        response = requests.put(f"{BASE_URL}/shops/{empty_id}", json=updated_shop_data)
        
        # Al mandar el id vacío, estamos haciendo una request PUT a /shops/
        assert response.status_code == 405  # Method Not Allowed

        # Chequeamos el "appropriate error message":
        error_data = response.json() # Sabemos que la api utiliza formato json en response.
        assert "detail" in error_data
        assert isinstance(error_data["detail"], str)
        assert "Method Not Allowed" in error_data["detail"]


    # C23
    @pytest.mark.negative
    def test_update_shop_with_non_numerical_shop_id(self, shop_service):
        # shop id no numérico:
        non_numerical_shop_id = "shop123"
        
        # Datos válidos para actualizar:
        updated_shop_data = {
            "address": "Nueva Dirección",
            "manager": "Nuevo Manager"
        }
        
        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=non_numerical_shop_id,
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 422  # Unprocessable Entity
        
        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: int_parsing shop_id attribute." in response.data["detail"]

    # C70
    @pytest.mark.negative
    def test_update_shop_with_negative_shop_id(self, shop_service):
        # shop id negativo:
        negative_shop_id = -1
        
        # Datos válidos para actualizar:
        updated_shop_data = {
            "address": "Nueva Dirección",
            "manager": "Nuevo Manager"
        }
        
        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=negative_shop_id,
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 404  # Not Found
        
        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]


    # C16
    @pytest.mark.negative
    def test_update_shop_with_required_attributes_empty(self, shop_service, created_shop):
       
       # Datos nuevos pero con atributos required vacíos:
        updated_shop_data_with_empty_required_attributes = {
            "address": "",  # Campo obligatorio vacío
            "manager": ""   # Campo obligatorio vacío
        }
        
        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data_with_empty_required_attributes,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 422  # Unprocessable Entity
        
        # Verificar mensaje de error apropiado:
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        
        # La api valida secuencialmente, por lo cuál solo aparece el error del campo vacío ḿas inmediato.
        detail_messages = response.data["detail"]
        assert "Address is required" in detail_messages or "Manager is required" in detail_messages
        # "Manager is required" NO aparecerá porque address vacío falla primero.


    # C88
    @pytest.mark.smoke
    def test_update_shop_with_new_address(self, shop_service, created_shop):
        # Solo actualizamos address (dejamos manager igual):
        updated_shop_data = {
            "address": "Nueva Dirección Solo Address",
            "manager": created_shop["manager"]  # Mantenemos el manager original.
        }
        
        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 200  # Ok
    
        # Verificamos estructura válida del shop actualizado:
        updated_shop = response.data
        
        assert "id" in updated_shop
        assert "address" in updated_shop
        assert "manager" in updated_shop
        assert "movies" in updated_shop
        
        # Verificamos tipos de datos:
        assert isinstance(updated_shop["id"], int)
        assert isinstance(updated_shop["address"], str)
        assert isinstance(updated_shop["manager"], str)
        assert isinstance(updated_shop["movies"], list)
        
        # Verificamos que los datos se actualizaron correctamente:
        assert updated_shop["id"] == created_shop["id"]  # id no cambia.
        assert updated_shop["address"] == updated_shop_data["address"]  # Address SÍ cambió.
        assert updated_shop["manager"] == created_shop["manager"]  # Manager NO cambió.
        assert updated_shop["movies"] == created_shop["movies"]  # Movies NO cambia.


    # C89
    @pytest.mark.smoke
    def test_update_shop_with_new_manager(self, shop_service, created_shop):
        # Solo actualizamos manager (dejamos address igual):
        updated_shop_data = {
            "address": created_shop["address"], # Mantenemos el address original.
            "manager": "Manager nuevo" 
        }
        
        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 200  # Ok
    
        # Verificamos estructura válida del shop actualizado:
        updated_shop = response.data
        
        assert "id" in updated_shop
        assert "address" in updated_shop
        assert "manager" in updated_shop
        assert "movies" in updated_shop
        
        # Verificamos tipos de datos:
        assert isinstance(updated_shop["id"], int)
        assert isinstance(updated_shop["address"], str)
        assert isinstance(updated_shop["manager"], str)
        assert isinstance(updated_shop["movies"], list)
        
        # Verificamos que los datos se actualizaron correctamente:
        assert updated_shop["id"] == created_shop["id"]  # id no cambia.
        assert updated_shop["address"] == created_shop["address"]  # Address NO cambió.
        assert updated_shop["manager"] == updated_shop_data["manager"]  # Manager SÍ cambió.
        assert updated_shop["movies"] == created_shop["movies"]  # Movies NO cambia.

    # C21
    @pytest.mark.negative
    def test_update_shop_with_empty_address(self, shop_service, created_shop):
        # Datos con address vacío pero manager válido:
        updated_shop_data = {
            "address": "",  # Campo obligatorio vacío
            "manager": "Manager Válido"  # Campo válido (para que el error sea específico de address)
        }
        
        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 422  # Unprocessable Entity
        
        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Address is required" in response.data["detail"]


    # C17
    @pytest.mark.negative
    def test_update_shop_with_empty_manager(self, shop_service, created_shop):
        # Datos con manager vacío pero address válido:
        updated_shop_data = {
            "address": "address válido", # Campo válido (para que el error sea específico de manager)
            "manager": ""  # Campo obligatorio vacío
        }

        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 422  # Unprocessable Entity
        
        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Manager is required" in response.data["detail"]


    # C65
    @pytest.mark.negative
    def test_update_shop_without_address(self, shop_service, created_shop):
        # Datos sólo con manager válido:
        updated_shop_data = {
            # Campo obligatorio "address" AUSENTE.
            "manager": "Manager Válido"  # Campo válido (para que el error sea específico de address).
        }
        
        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 422  # Unprocessable Entity
        
        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: missing address attribute." in response.data["detail"]

    # C64
    @pytest.mark.negative
    def test_update_shop_without_manager(self, shop_service, created_shop):
        # Datos sólo con address válido:
        updated_shop_data = {
            "address" : "address válido" # Campo válido (para que el error sea específico de address).
            # Campo obligatorio "manager" AUSENTE.
        }
        
        # Hacemos la consulta (update):
        response = shop_service.update_shop(
            shop_id=created_shop["id"],
            shop_data=updated_shop_data,
            response_type=dict
        )
        
        # Verificaciones:
        assert response.status == 422  # Unprocessable Entity
        
        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: missing manager attribute." in response.data["detail"]

    