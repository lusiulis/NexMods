from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import Product, ProductVariant, ImageSet, Category
from app.schemas import ProductCreate, ProductOut, PaginatedProductSummaryOut, ProductSummaryOut
from sqlalchemy.orm import selectinload
from typing import Optional, List

async def create_product(db: AsyncSession, data: ProductCreate) -> ProductOut:
    product = Product(
        name=data.name,
        description=data.description,
        sell_count=data.sell_count
    )
    for var_in in data.variants:
        variant = ProductVariant(
            name = var_in.name,
            description = var_in.description,
            price = var_in.price
        )
        for img_in in var_in.images:
            variant.images.append(ImageSet(
                url=img_in.url
            ))
        product.variants.append(variant)
    
    db.add(product)
    await db.commit()
    
    result = await db.execute(
        select(Product)
        .where(Product.id == product.id)
        .options(
            selectinload(Product.variants)
            .selectinload(ProductVariant.images)
        )
    )
    product_with_relations = result.scalar_one()
    return ProductOut.model_validate(product_with_relations)

async def get_products(
    db: AsyncSession, 
    page: int = 1,
    limit: int = 10,
    category: Optional[str] = None,
    name: Optional[str] = None
) -> PaginatedProductSummaryOut:
    offset = (page - 1) * limit
    
    query = select(Product).options(
        selectinload(Product.variants).selectinload(ProductVariant.images)
    )
    
    if name:
        query = query.where(Product.name.ilike(f"%{name}%"))
    
    if category:
        query = query.join(Product.categories).where(Category.name == category)
    
    total_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = total_result.scalar() or 0
    pages = (total + limit -1) // limit
    
    result = await db.execute(query.offset(offset).limit(limit))
    products: List[Product] = list(result.scalars().all())
    
    items = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.variants[0].price if p.variants else 0,
            "image_url": p.variants[0].images[0].url if (p.variants and p.variants[0].images) else ""
        }
        for p in products
    ]
    
    return PaginatedProductSummaryOut(
        total = total,
        pages = pages,
        items = items
    )