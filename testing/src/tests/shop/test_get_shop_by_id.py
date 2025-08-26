import os
import sys
import pytest
import requests  ## Para poder automatizar "id vacío" y "sin id".

from dotenv import load_dotenv
load_dotenv()  # Esto carga las variables del .env
BASE_URL = os.getenv("BASE_URL")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

class TestGetShopById:  # Faltan: C3 y C4 (Que son de Read All Shops)

    # C10
    @pytest.mark.smoke
    def test_read_shop_by_id_with_an_existing_shop_id(self, shop_service, created_shop):
        # Hacemos la consulta (habiendo creado previamente el shop):
        response = shop_service.get_shop_by_id(shop_id=created_shop["id"], response_type=dict)

        # Verificaciones
        assert response.status == 200 # Ok

        # Verificamos estructura válida del shop:
        shop = response.data # Para poder manipularlo mejor.

        assert "id" in shop
        assert "address" in shop
        assert "manager" in shop
        assert "movies" in shop

        # Verificamos tipos de datos de los atributos de shop:
        assert isinstance(shop["id"], int)
        assert isinstance(shop["address"], str)
        assert isinstance(shop["manager"], str)
        assert isinstance(shop["movies"], list)

        # Verificar que coincide con el shop creado (pueden pasar cosas en medio):
        assert shop["id"] == created_shop["id"]
        assert shop["address"] == created_shop["address"]
        assert shop["manager"] == created_shop["manager"]
    

    # # C12    
    @pytest.mark.negative
    def test_read_shop_by_id_with_a_non_existent_shop_id(self, shop_service):
        # shop id que no existe:
        non_existent_shop_id = 99999

        # Hacemos la consulta:
        response = shop_service.get_shop_by_id(shop_id=non_existent_shop_id, response_type=dict)

        # Verificaciones:
        assert response.status == 404 # Not Found

        # Chequeamos el "appropriate error message":
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]


    # # C13 - "id vacío"   
    @pytest.mark.negative
    def test_read_shop_by_id_with_empty_shop_id(self):
        # shop id vacío:
        empty_id = ""

        # Hacemos la consulta:
        response = requests.get(f"{BASE_URL}/shops/{empty_id}")

        # Al mandar el id vacío, simplemente estamos consultando otro endpoint: ( .../shops/)
        assert response.status_code in [404, 405, 200] # "Not Found", "Method Not Allowed", "Ok".

        # -> Siempre se obtiene 200 Ok, porque la consulta se termina realizando en otro endpoint.

    # C24    
    @pytest.mark.negative
    def test_read_shop_by_id_with_a_non_numerical_shop_id(self, shop_service):
        # shop id no numérico:
        non_numerical_shop_id = "shop45"

        # Hacemos la consulta:
        response = shop_service.get_shop_by_id(shop_id=non_numerical_shop_id, response_type=dict)

        # Verificaciones:
        assert response.status == 422 # Unprocessable Entity

        # Verificar el mensaje de validación apropriado
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Validation Error: int_parsing shop_id attribute." in response.data["detail"]


    # C67 - "Sin id"    
    @pytest.mark.negative
    def test_read_shop_by_id_without_shop_id(self):

        # Hacemos la consulta "sin id":
        response = requests.get(f"{BASE_URL}/shops/")

        # Al NO mandar el id, otra vez, estamos consultando otro endpoint: ( .../shops/)
        assert response.status_code in [404, 405, 200] # "Not Found", "Method Not Allowed", "Ok".

        # -> Siempre se obtiene 200 Ok, porque la consulta se termina realizando en otro endpoint.


    # C69
    @pytest.mark.negative
    def test_read_shop_by_id_with_a_negative_shop_id(self, shop_service):
        # shop id negativo:
        negative_shop_id = -1

        # Hacemos la consulta:
        response = shop_service.get_shop_by_id(shop_id=negative_shop_id, response_type=dict)

        # Verificaciones:
        assert response.status == 404 # Not Found

        # Chequeamos el "appropriate error message"
        assert "detail" in response.data
        assert isinstance(response.data["detail"], list)
        assert "Shop Not Found" in response.data["detail"]


