from fastapi import APIRouter, Query, Depends
from app.schemas import PaginatedCategorySummaryOut, CategoryOut, CategoryCreate, ActionResponse, CategoryUpdate, CategoryProductLinkIn
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.category import get_categories, create_category, delete_category, update_category, link_category_product, unlink_category_product
from typing import Optional
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=PaginatedCategorySummaryOut)
async def get(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Page's items quantity"),
    name: Optional[str] = Query(None, description="Name filter"),
):
    return await get_categories(db, page, limit, name)

@router.post("/", response_model=CategoryOut)
async def create(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_category(db, data)

@router.delete("/{id}", response_model=ActionResponse)
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_category(db, id)

@router.patch("/{id}", response_model=ActionResponse)
async def update(id: int, data: CategoryUpdate, db: AsyncSession = Depends(get_db)):
    return await update_category(db, id, data)

@router.post("/link", response_model=ActionResponse)
async def create_category_product_link(data: CategoryProductLinkIn, db: AsyncSession = Depends(get_db)):
    return await link_category_product(db, data)

@router.delete("/link", response_model=ActionResponse)
async def delete_category_product_link(data: CategoryProductLinkIn, db: AsyncSession = Depends(get_db)):
    return await unlink_category_product(db, data)