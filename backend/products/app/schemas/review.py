from pydantic import BaseModel, Field
from .utils import PaginatedModel
from typing import List, Optional

class ReviewCreate(BaseModel):
    user_id: int
    product_id: int
    rating: int = Field(ge=1, le=5)
    comment: str
    
class ReviewOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int = Field(ge=1, le=5)
    comment: str
    
    model_config = {
        "from_attributes": True
    }
    
class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(ge=1, le=5)
    comment: Optional[str]

 #--------------------------------------------#   
 
class ReviewUserInfo(BaseModel):
    id: int
    username: str
    profile_img: str
 
class ReviewItem(BaseModel):
    id: int
    rating: int = Field(ge=1, le=5)
    comment: str
    user: ReviewUserInfo
    
    model_config = {
        "from_attributes": True
    }
    
class PaginatedReviewItem(PaginatedModel):
    items: List[ReviewItem] = []