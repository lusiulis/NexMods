from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, insert, delete
from app.schemas import CategoryCreate, CategoryOut, CategoryUpdate, ActionResponse, PaginatedCategorySummaryOut, CategorySummaryOut, CategoryProductLinkIn
from app.models import Category
from app.models import Product, ProductStatus, categoryxproduct
from typing import Optional
from fastapi import HTTPException

async def create_category(
    db: AsyncSession,
    data: CategoryCreate
) -> CategoryOut:
    result = await db.execute(select(Category).where(Category.name == data.name))
    category_with_name = result.scalar_one_or_none()
    if category_with_name:
        raise HTTPException(status_code=409, detail="Category name already taken.")
    
    new_category = Category(
        name=data.name,
        description=data.description
    )
    
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
        
    return CategoryOut.model_validate(new_category)

async def update_category(
    db: AsyncSession,
    id: int,
    data: CategoryUpdate
) -> ActionResponse:
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    
    if data.name:
        name_query_result = await db.execute(select(Category).where(Category.name == data.name))
        category_with_name = name_query_result.scalar_one_or_none()
        if category_with_name and category_with_name.id != id:
            raise HTTPException(status_code=409, detail="Category name already taken.")
        
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
        
    db.add(category)
    await db.commit()
    await db.refresh(category)
        
    return ActionResponse(
        message = "Category updated successfully",
        status = "successful"
    )
    
async def delete_category(
    db: AsyncSession,
    id: int
) -> ActionResponse:
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    
    #Check relations with Product
    
    await db.delete(category)
    await db.commit()
    
    return ActionResponse(
        message = "Category deleted successfully",
        status = "successful"
    )
    
async def get_categories(
    db: AsyncSession,
    page: int = 1,
    limit: int = 10,
    name: Optional[str] = None
) -> PaginatedCategorySummaryOut:
    offset = (page - 1) * limit 
    query = select(Category)
    if name:
        query = query.where(Category.name.ilike(f"%{name}%"))
        
    total_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = total_result.scalar() or 0
    pages = (total + limit - 1) // limit
    
    count_expr = func.count(Product.id).filter(Product.status == ProductStatus.ACTIVE)
    stmt = (
        select(
            Category.id,
            Category.name,
            Category.description,
            count_expr.label("product_count")
        )
        .outerjoin(Category.products)
        .group_by(Category.id)
        .order_by(Category.name)
        .offset(offset)
        .limit(limit)
    )
    
    rows = (await db.execute(stmt)).all()
    
    items = [
        CategorySummaryOut(
            id = row[0],
            description = row[2],
            name = row[1],
            product_count= row[3] or 0
        )
        for row in rows
    ]

    return PaginatedCategorySummaryOut(
        total=total,
        pages=pages,
        items=items
    )
    
async def link_category_product(
    db: AsyncSession,
    data: CategoryProductLinkIn
) -> ActionResponse:
    cat = await db.get(Category, data.category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    
    prod = await db.get(Product, data.product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    
    result = await db.execute(
        select(categoryxproduct).where(
            categoryxproduct.c.category_id == data.category_id,
            categoryxproduct.c.product_id == data.product_id
        )
    )
    if result.first():
        raise HTTPException(status_code=400, detail="Relation already exists")

    await db.execute(
        insert(categoryxproduct).values(
            category_id=data.category_id,
            product_id=data.product_id
        )
    )
    await db.commit()

    return ActionResponse(
        message = "Category linked to product successfully",
        status = "successful"
    )
    
async def unlink_category_product(
    db: AsyncSession,
    data: CategoryProductLinkIn
) -> ActionResponse:
    result = await db.execute(
        delete(categoryxproduct).where(
            categoryxproduct.c.category_id == data.category_id,
            categoryxproduct.c.product_id == data.product_id
        )
    )

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Relation not found")

    await db.commit()
    
    return ActionResponse(
        message = "Category unlinked to product successfully",
        status = "successful"
    ) 