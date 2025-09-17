from pydantic import BaseModel

class AddShopModel(BaseModel):
    address: str
    manager: str

