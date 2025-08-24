from sqlalchemy import Integer, String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.associations import categoryxproduct
from typing import List
import enum

class ProductStatus(enum.Enum):
    ACTIVE = "active"
    DELETED = "deleted"

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus), nullable=False, default=ProductStatus.ACTIVE)
    sell_count: Mapped[int] = mapped_column(Integer, nullable=False)
    
    variants: Mapped[List["ProductVariant"]] = relationship("ProductVariant", back_populates="product")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="product")
    categories: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="products",
        secondary=categoryxproduct,
    )
    
    
class ProductVariant(Base):
    __tablename__ = "product_variants"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ProductStatus] = mapped_column(Enum(ProductStatus), nullable=False, default=ProductStatus.ACTIVE)
    
    product = relationship("Product", back_populates="variants")
    carts: Mapped[List["Cart"]] = relationship("Cart", back_populates="product_variant")
    images: Mapped[List["ImageSet"]] = relationship("ImageSet", back_populates="variant")
    
class ImageSet(Base):
    __tablename__ = "image_sets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    variant_id: Mapped[int] = mapped_column(Integer, ForeignKey("product_variants.id"), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    
    variant = relationship("ProductVariant", back_populates="images")
    
    