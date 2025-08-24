from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from app.models import Product, ProductVariant, ImageSet, Category, ProductStatus
from app.schemas import ProductCreate, ProductOut, PaginatedProductSummaryOut, ProductSummaryOut, ProductSimpleOut, ProductUpdate, ProductVariantCreate, ProductVariantOut, ProductVariantSimpleOut, ProductVariantUpdate, ImageSetCreate, ImageSetOut, ActionResponse
from sqlalchemy.orm import selectinload, with_loader_criteria
from fastapi import HTTPException
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
    query = select(Product).where(Product.status == ProductStatus.ACTIVE).options(
        selectinload(Product.variants).selectinload(ProductVariant.images),
        with_loader_criteria(ProductVariant, ProductVariant.status == ProductStatus.ACTIVE)
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
        ProductSummaryOut(
            id = p.id,
            status = p.status,
            name = p.name,
            price =p.variants[0].price if p.variants else 0,
            images = [v.images[0].url for v in p.variants if v.images and v.images[0]]
        )
        for p in products
    ]
    
    return PaginatedProductSummaryOut(
        total= total,
        pages= pages,
        items= items
    )
    
async def get_product_detail(
    db: AsyncSession,
    id: int
) -> ProductOut: 
    query = select(Product).where(Product.id == id).options(
        selectinload(Product.variants).selectinload(ProductVariant.images),
        with_loader_criteria(ProductVariant, ProductVariant.status == ProductStatus.ACTIVE)
    )
    result = await db.execute(query)
    product_with_relations = result.scalar_one_or_none()
    
    if not product_with_relations:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    return ProductOut.model_validate(product_with_relations)

async def delete_product(
    db: AsyncSession,
    id: int
) -> ProductSimpleOut:
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    product.status = ProductStatus.DELETED
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

async def update_product(
    db: AsyncSession,
    id: int,
    data: ProductUpdate
) -> ProductSimpleOut:
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
        
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

#------------------------------------------------------------------------------

async def add_product_variant(
    db: AsyncSession,
    id: int,
    data: ProductVariantCreate
) -> ProductVariantOut:
    result = await db.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    variant = ProductVariant(
        name = data.name,
        description = data.description,
        price = data.price,
        product_id = id
    )
    for img in data.images:
        variant.images.append(ImageSet(
            url=img.url
        ))
    
    db.add(variant)
    await db.commit()
    variant_query = await db.execute(
        select(ProductVariant)
        .where(ProductVariant.id == variant.id)
        .options(selectinload(ProductVariant.images))
    )
    variant_with_images = variant_query.scalar_one()
    return ProductVariantOut.model_validate(variant_with_images)

async def delete_product_variant(
    db: AsyncSession,
    id: int
) -> ProductVariantSimpleOut:
    result = await db.execute(select(ProductVariant).where(ProductVariant.id == id))
    variant = result.scalar_one_or_none()
    if not variant:
        raise HTTPException(status_code=404, detail="ProductVariant not found.")
    
    variant.status = ProductStatus.DELETED
    db.add(variant)
    await db.commit()
    await db.refresh(variant)
    return variant

async def update_product_variant(
    db: AsyncSession,
    id: int,
    data: ProductVariantUpdate
) -> ProductVariantSimpleOut:
    result = await db.execute(select(ProductVariant).where(ProductVariant.id == id))
    variant = result.scalar_one_or_none()
    if not variant:
        raise HTTPException(status_code=404, detail="ProductVariant not found.")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(variant, field, value)
    
    db.add(variant)
    await db.commit()
    await db.refresh(variant)
    return variant

#------------------------------------------------------------------------------

async def add_variant_image(
    db: AsyncSession,
    id: int,
    data: ImageSetCreate
) -> ImageSetOut:
    result = await db.execute(select(ProductVariant).where(ProductVariant.id == id))
    variant = result.scalar_one_or_none()
    if not variant:
        raise HTTPException(status_code=404, detail="ProductVariant not found.")
    
    image = ImageSet(
        url = data.url,
        variant = variant
    )
    
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image

async def delete_variant_image(
    db: AsyncSession,
    id: int
) -> ActionResponse:
    result = await db.execute(select(ImageSet).where(ImageSet.id == id))
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="ImageSet not found.")
    
    await db.delete(image)
    await db.commit()
    
    return ActionResponse(
        message = "Image deleted successfully",
        status = "successful"
    )