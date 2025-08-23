from pydantic import BaseModel
from .pagination import PaginatedModel
from typing import List
    
class ImageSetCreate(BaseModel):
    url: str    
    
class ProductVariantCreate(BaseModel):
    name: str
    description: str
    price: int
    images: List[ImageSetCreate] = []

class ProductCreate(BaseModel):
    name: str
    description: str
    sell_count: int
    variants: List[ProductVariantCreate] = []
    
#--------------------------------------------#

class ImageSetOut(BaseModel):
    id: int
    url: str    
    
    model_config = {
        "from_attributes": True
    }
        
class ProductVariantOut(BaseModel):
    id: int
    name: str
    description: str
    price: int
    images: List[ImageSetOut] = []
    
    model_config = {
        "from_attributes": True
    }
    
class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    sell_count: int
    variants: List[ProductVariantOut] = []
    
    model_config = {
        "from_attributes": True
    }

    
class ProductSummaryOut(BaseModel):
    id: int
    name: str
    price: int
    image_url: str
    
    model_config = {"from_attributes": True}
    
class PaginatedProductSummaryOut(PaginatedModel):
    items: List[ProductSummaryOut] = []
    
    model_config = {"from_attributes": True}