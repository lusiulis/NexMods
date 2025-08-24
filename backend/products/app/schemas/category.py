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
    products_count: int
    
    model_config = {
        "from_attributes": True
    }
    
class PaginatedCategorySummaryOut(PaginatedModel):
    items: List[CategoryOut] = []
    
