from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    desciption: str
    price: float
    
class ProductOut(ProductCreate):
    id: int