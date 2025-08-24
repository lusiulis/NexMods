from sqlalchemy import Table, Column, ForeignKey
from app.database import Base

categoryxproduct = Table(
    "categoryxproduct",
    Base.metadata,
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
)
