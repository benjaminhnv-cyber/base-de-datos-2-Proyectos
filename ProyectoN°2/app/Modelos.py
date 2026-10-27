from decimal import Decimal
from datetime import datetime, timezone
from sqlalchemy import String, Numeric, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(1050), nullable=True)

    # Relaciones
    products: Mapped[list["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1050), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relación con Category
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True, default=None)
    category: Mapped["Category | None"] = relationship(back_populates="products")

class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)  

    #Relaciones
    orders: Mapped[list["Order"]] = relationship(back_populates="table")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="abierto", nullable=False) 
    notes: Mapped[str | None] = mapped_column(String(250), nullable=True)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), nullable=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relaciones
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"), nullable=False)
    table: Mapped["Table"] = relationship(back_populates="orders")
    details: Mapped[list["OrderDetail"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderDetail(Base):
    __tablename__ = "order_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    #Relaciones
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    order: Mapped["Order"] = relationship(back_populates="details")
    product: Mapped["Product"] = relationship()