from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

class Product_create(BaseModel):
    name: str = Field(..., min_length=1, max_length=250)
    description: Optional[str] = Field(None, max_length=1050)
    price: Decimal = Field(..., gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="El stock no puede ser negativo")
    availability: bool = True
    category_id: Optional[int] = Field(None, gt=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=250)
    description: Optional[str] = Field(None, max_length=1050)
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    availability: Optional[bool] = None
    category_id: Optional[int] = Field(None, gt=0)

class Product_activate(BaseModel):
    availability: bool = True

class Catagory_create(BaseModel):
    name: str = Field(..., min_length=1, max_length=250)
    description: Optional[str] = Field(None, max_length=1050)

class Table_create(BaseModel):
    number: int = Field(..., gt=0)
    capacity: int = Field(..., gt=0)
    availability: bool = True

class Table_update(BaseModel):
    capacity: Optional[int] = Field(None, gt=0)
    availability: Optional[bool] = None

class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

class Order_create(BaseModel):
    table_id: int = Field(..., gt=0)
    notes: Optional[str] = Field(None, max_length=250)
    items: list[OrderItemCreate] = Field(..., min_items=1)

# Reportes
class SalesReportResponse(BaseModel):
    fecha: date
    total_ventas: Decimal
    cantidad_pedidos: int

class TopProductResponse(BaseModel):
    product_id: int
    name: str
    total_vendido: int

class TableStatusDetail(BaseModel):
    number: int
    capacity: int
    estado: str

class TablesStatusResponse(BaseModel):
    total_mesas: int
    mesas_libres: int
    mesas_ocupadas: int
    detalle: list[TableStatusDetail]