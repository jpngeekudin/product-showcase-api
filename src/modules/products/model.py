from pydantic import BaseModel


class ProductModel(BaseModel):
    name: str
    category: str
    stock: int
    price: int
    description: str
    image: str
