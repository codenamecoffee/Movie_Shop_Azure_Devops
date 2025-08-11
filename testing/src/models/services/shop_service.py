from typing import Type
from src.base.service_base import ServiceBase
from src.models.responses.base.response import T, Response
from src.models.requests.shop.add_shop_model import AddShopModel


class ShopService(ServiceBase):
    def __init__(self):
        super().__init__("shops")

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
