from pydantic import BaseModel

class PaginatedModel(BaseModel):
    total: int
    pages: int
    
class ActionResponse(BaseModel):
    status: str
    message: str