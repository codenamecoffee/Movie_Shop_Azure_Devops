from typing import Type
from src.base.service_base import ServiceBase
from src.models.responses.base.response import T, Response

from src.models.requests.shop.add_shop_model import AddShopModel

class ShopService(ServiceBase):
    def __init__(self, base_url: str = ""):
        super().__init__("shops", base_url=base_url)

    def add_shop(
        self,
        shop: AddShopModel,
        response_type: Type[T],
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.post(
            self.url,
            shop,
            config=config,
            response_model=response_type,
        )

    def get_shops(self, response_type: Type[T], config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.get(
            f"{self.url}",
            config=config,
            response_model=response_type,
        )

    def get_shop_by_id(self, shop_id: int, response_type: Type[T], config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.get(
            f"{self.url}/{shop_id}",
            config=config,
            response_model=response_type,
        )

    def create_shop(
        self,
        shop: AddShopModel,
        response_type: Type[T],
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.post(
            self.url,
            shop.model_dump(),
            config=config,
            response_model=response_type,
        )
    def update_shop(
        self,
        shop_id: int,
        shop: AddShopModel,  # o UpdateShopModel si creaste uno separado
        response_type: Type[T] = None,
        config: dict | None = None
    ) -> Response[T]:
        config = config or self.default_config
        return self.put(
            f"{self.url}/{shop_id}",
            shop.model_dump(),  # convertimos a dict
            config=config,
            response_model=response_type,
        )

    def delete_shop(self, shop_id: int, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.delete(
            f"{self.url}/{shop_id}",
            config=config,
            response_model=response_type,
        )

    def get_movies_by_shop(self, shop_id: int, response_type: Type[T], config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.get(
            f"{self.url}/{shop_id}/movies",
            config=config,
            response_model=response_type,
        )

    def get_available_movies_by_shop(self, shop_id: int, response_type: Type[T], config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.get(
            f"{self.url}/{shop_id}/available-movies",
            config=config,
            response_model=response_type,
        )
