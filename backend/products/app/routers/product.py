from fastapi import APIRouter, Depends, Query
from app.schemas import ProductOut, ProductCreate, PaginatedProductSummaryOut, ProductSimpleOut, ProductUpdate, ProductVariantCreate, ProductVariantOut, ProductVariantSimpleOut, ProductVariantUpdate, ImageSetOut, ImageSetCreate, ActionResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product import create_product, get_products, get_product_detail, delete_product, update_product, add_product_variant, delete_product_variant, update_product_variant, add_variant_image, delete_variant_image
from app.database import get_db
from typing import Optional

router = APIRouter()

@router.post("/", response_model=ProductOut)
async def create(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, data)

@router.get("/", response_model=PaginatedProductSummaryOut)
async def get(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Page's items quantity"),
    category: Optional[str] = Query(None, description="Category filter"),
    name: Optional[str] = Query(None, description="Name filter"),
):
    return await get_products(db, page, limit, category, name)

@router.get("/{id}", response_model=ProductOut)
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
    return await get_product_detail(db, id)

#Add admin get {id} to handle deleted product variants

@router.delete("/{id}", response_model=ProductSimpleOut)
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_product(db, id)

@router.patch("/{id}", response_model=ProductSimpleOut)
async def update(id: int, data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    return await update_product(db, id, data)

#----------------------------------------------------------------------------------------

@router.post("/{id}/variants", response_model=ProductVariantOut)
async def create_variant(id: int, data: ProductVariantCreate, db: AsyncSession = Depends(get_db)):
    return await add_product_variant(db, id, data)

@router.delete("/variants/{id}", response_model=ProductVariantSimpleOut)
async def delete_variant(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_product_variant(db, id)

@router.patch("/variants/{id}", response_model=ProductVariantSimpleOut)
async def update_variant(id: int, data: ProductVariantUpdate, db: AsyncSession = Depends(get_db)):
    return await update_product_variant(db, id, data)

#----------------------------------------------------------------------------------------

@router.post("/variant/{id}/images", response_model=ImageSetOut)
async def create_image(id: int, data: ImageSetCreate, db: AsyncSession = Depends(get_db)):
    return await add_variant_image(db, id, data)

@router.delete("/variant/images/{id}", response_model=ActionResponse)
async def delete_image(id: int, db: AsyncSession = Depends(get_db)):
    return await delete_variant_image(db, id)