from typing import Type
from src.base.service_base import ServiceBase
from src.models.responses.base.response import T, Response


class ShopService(ServiceBase):
    def __init__(self, base_url: str = ""):
        super().__init__("shops", base_url=base_url)

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

    def create_shop(self, shop_data: dict, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.post(
            f"{self.url}",
            data=shop_data,
            config=config,
            response_model=response_type,
        )

    def update_shop(self, shop_id: int, shop_data: dict, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.put(
            f"{self.url}/{shop_id}",
            data=shop_data,
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
