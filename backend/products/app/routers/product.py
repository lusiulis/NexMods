from fastapi import APIRouter, Depends, Query
from app.schemas.product import ProductOut, ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product import create_product, get_products
from app.database import get_db
from typing import List, Optional
router = APIRouter()

@router.post("/", response_model=ProductOut)
async def create(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, data)

@router.get("/", response_model=List[ProductOut])
async def get(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Page's items quantity"),
    category: Optional[str] = Query(None, description="Category filter"),
    name: Optional[str] = Query(None, description="Name filter"),
):
    return await get_products(db, page, limit, category, name)