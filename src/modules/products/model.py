from pydantic import BaseModel

class ProductModel(BaseModel):
    name: str
    cateogry: str
    stock: int
    price: int