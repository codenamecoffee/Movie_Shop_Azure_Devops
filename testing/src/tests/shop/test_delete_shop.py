import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.responses.base.response import Response

class TestDeleteShop: 
      
     #C26 
    @pytest.mark.smoke #caso correcto
    def test_delete_shop_with_correct_id(self, shop_service, created_shop):
        """C26: Eliminar un shop existente → 204"""
        response = shop_service.delete_shop(shop_id=created_shop["id"])
        assert response.status == 204

    #C27
    @pytest.mark.negative #inexistente
    def test_delete_shop_with_nonexistent_id(self, shop_service):
        invalid_shop_id = 99999
        response = shop_service.delete_shop(shop_id=invalid_shop_id)
        assert response.status == 404

