from pydantic import BaseModel
from .utils import PaginatedModel
from app.models import ProductStatus
from typing import List, Optional
    
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
    status: ProductStatus
    images: List[ImageSetOut] = []
    
    model_config = {
        "from_attributes": True
    }
    
class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    sell_count: int
    status: ProductStatus
    variants: List[ProductVariantOut] = []
    
    model_config = {
        "from_attributes": True
    }
    
#--------------------------------------------#

class ProductSimpleOut(BaseModel):
    id: int
    name: str
    description: str
    sell_count: int
    status: ProductStatus
    
    model_config = {
        "from_attributes": True
    }
    
class ProductVariantSimpleOut(BaseModel):
    id: int
    name: str
    description: str
    price: int
    status: ProductStatus
    
    model_config = {
        "from_attributes": True
    }

 #--------------------------------------------#   
    
class ProductSummaryOut(BaseModel):
    id: int
    name: str
    price: int
    status: ProductStatus
    images: List[str] = []
    
class PaginatedProductSummaryOut(PaginatedModel):
    items: List[ProductSummaryOut] = []

#--------------------------------------------#

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    sell_count: Optional[int] = None
    status: Optional[ProductStatus] = None
    
class ProductVariantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    status: Optional[ProductStatus] = None
    

