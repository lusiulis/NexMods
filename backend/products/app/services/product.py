from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.product import Product
from app.schemas.product import ProductCreate
from typing import Optional

async def create_product(db: AsyncSession, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

async def get_products(
    db: AsyncSession, 
    page: int = 1,
    limit: int = 10,
    category: Optional[str] = None,
    name: Optional[str] = None
):
    query = select(Product)
    #if category:
    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))
    
    total_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(total_query)
    total = total_result.scalar() or 0
    
    query = query.offset((page - 1) * limit).limit(limit)
    
    result = await db.execute(query)
    products = result.scalars().all()
    
    return {
        "items": products,
        "total": total,
        "page": page,
        "pages": (total + limit - 1)
    }