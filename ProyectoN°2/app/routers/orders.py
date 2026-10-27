from decimal import Decimal
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Importar la fábrica de sesiones desde database.py
from database import Session
from Modelos import Order, OrderDetail, Product, Table
from schemas import Order_create

router = APIRouter(prefix="/orders", tags=["Order"])


@router.get("", status_code=200)
def listado_ordenes(status_filter: Optional[str] = Query(None, alias="status", description="Filtrar por estado (ej: abierto, pagado)"), min_total: Optional[Decimal] = Query(None, ge=0, description="Filtrar por monto total mínimo")):
    with Session() as session:
        query = select(Order).options(selectinload(Order.details))

        if status_filter:
            query = query.where(Order.status == status_filter)

        if min_total is not None:
            query = query.where(Order.total >= min_total)

        ordenes = session.execute(query).scalars().all()
        return ordenes

@router.post("", status_code=201)
def crear_orden(ord: Order_create):
    with Session() as session:
        table = session.get(Table, ord.table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")
        
        if not table.availability:
            raise HTTPException(status_code=400, detail=f"La mesa número {table.number} ya está ocupada.")

        # Validación explícita de pedido abierto existente
        pedido_abierto = session.execute(select(Order).where(Order.table_id == ord.table_id, Order.status == "abierto")).scalar_one_or_none()
        
        if pedido_abierto:
            raise HTTPException(status_code=400, detail="La mesa ya tiene un pedido abierto registrado.")

        table.availability = False
        new_order = Order(table_id=ord.table_id, notes=ord.notes, status="abierto", total=Decimal("0.00"))
        session.add(new_order)
        session.flush()

        total_calculado = Decimal("0.00")
        for item in ord.items:
            producto = session.get(Product, item.product_id)
            if not producto or not producto.availability:
                raise HTTPException(status_code=400, detail=f"El producto con ID {item.product_id} no está disponible.")
            
            if producto.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Stock insuficiente para '{producto.name}'. Disponible: {producto.stock}")

            producto.stock -= item.quantity
            if producto.stock == 0:
                producto.availability = False 

            subtotal = producto.price * item.quantity
            total_calculado += subtotal
            detail = OrderDetail(order_id=new_order.id, product_id=producto.id, quantity=item.quantity, unit_price=producto.price, subtotal=subtotal)
            session.add(detail)

        new_order.total = total_calculado
        session.commit()
        session.refresh(new_order)
        return new_order


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
def obtener_orden(order_id: int):
    with Session() as session:
        order = session.execute(select(Order).options(selectinload(Order.details)).where(Order.id == order_id)).scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        return order


@router.post("/{order_id}/pay", status_code=status.HTTP_200_OK)
def pagar_orden(order_id: int):
    with Session() as session:
        order = session.execute(select(Order).options(selectinload(Order.details)).where(Order.id == order_id)).scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        if order.status != "abierto":
            raise HTTPException(status_code=400, detail=f"El pedido ya no está abierto (Estado actual: '{order.status}').")

        order.status = "pagado"
        mesa = session.get(Table, order.table_id)
        if mesa:
            mesa.availability = True

        session.commit()
        session.refresh(order)
        return order
