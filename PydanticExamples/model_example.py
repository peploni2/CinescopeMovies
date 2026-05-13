from pydantic import BaseModel
from enum import Enum

class Category(str, Enum):
    electronic = "Электроника"
    clothes = "Одежда"

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool
    category: Category

product = Product(name="Монитор", price=15000.99, in_stock=True, category=Category.electronic)

json_data = product.model_dump_json()
print(json_data)

new_product = Product.model_validate_json(json_data)
print(new_product)