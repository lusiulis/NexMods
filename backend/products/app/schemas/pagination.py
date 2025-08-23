from pydantic import BaseModel

class PaginatedModel(BaseModel):
    total: int
    pages: int
    model_config = {"from_attributes": True}