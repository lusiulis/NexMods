from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    sell_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    variants = relationship("ProductVariant", back_populates="product")
    
    
    
class ProductVariant(Base):
    __tablename__ = "product_variants"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    
    product = relationship("Product", back_populates="variants")
    images = relationship("ImageSet", back_populates="variant")
    
class ImageSet(Base):
    __tablename__ = "image_sets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    variant_id: Mapped[int] = mapped_column(Integer, ForeignKey("product_variants.id"), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    
    variant = relationship("ProductVariant", back_populates="images")
    
    