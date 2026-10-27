from datetime import date
from fastapi import APIRouter, Query
from sqlalchemy import func, select

# Importación de la conexión y modelos
from database import Session
from Modelos import Order, OrderDetail, Product, Table
from schemas import SalesReportResponse, TopProductResponse, TablesStatusResponse

router = APIRouter(prefix="/reports", tags=["Report"])

@router.get("/sales", status_code=200, response_model=SalesReportResponse) # Se agrega el response_model
def ventas_del_dia(fecha: date):
    with Session() as session:
        report = session.execute(select(func.coalesce(func.sum(Order.total), 0).label("total_ventas"),func.count(Order.id).label("cantidad_pedidos")).where(Order.status == "pagado", func.date(Order.date_creation) == fecha)).one()

        return {"fecha": fecha, "total_ventas": report.total_ventas, "cantidad_pedidos": report.cantidad_pedidos}
    
@router.get("/top-products", status_code=200, response_model=list[TopProductResponse])
def top_productos(
    limit: int = Query(5, gt=0, description="Cantidad de productos a retornar")
):
    with Session() as session:
        # Unir OrderDetail con Order (solo pagados) y agrupar por producto
        query = (select(Product.id.label("product_id"),Product.name.label("name"),func.sum(OrderDetail.quantity).label("total_vendido")).join(OrderDetail, Product.id == OrderDetail.product_id).join(Order, OrderDetail.order_id == Order.id).where(Order.status == "pagado").group_by(Product.id, Product.name).order_by(func.sum(OrderDetail.quantity).desc()).limit(limit))

        resultados = session.execute(query).all()
        return [{"product_id": r.product_id,"name": r.name,"total_vendido": r.total_vendido}for r in resultados]


@router.get("/tables-status", status_code=200, response_model=TablesStatusResponse)
def estado_mesas():
    with Session() as session:
        mesas = session.execute(select(Table)).scalars().all()
        
        libres = sum(1 for m in mesas if m.availability)
        ocupadas = len(mesas) - libres

        return {"total_mesas": len(mesas),"mesas_libres": libres,"mesas_ocupadas": ocupadas,"detalle": [{"number": m.number,"capacity": m.capacity,"estado": "libre" if m.availability else "ocupada"}for m in mesas]}