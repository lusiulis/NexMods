from pydantic import BaseModel
from .utils import PaginatedModel
from typing import List, Optional

class CategoryCreate(BaseModel):
    name: str
    description: str
    
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    
class CategoryOut(BaseModel):
    id: int
    name: str
    description: str
    
    model_config = {
        "from_attributes": True
    }
    
class CategorySummaryOut(BaseModel):
    id: int
    name: str
    description: str
    product_count: int
    
    model_config = {
        "from_attributes": True
    }
    
class PaginatedCategorySummaryOut(PaginatedModel):
    items: List[CategorySummaryOut] = []
    
