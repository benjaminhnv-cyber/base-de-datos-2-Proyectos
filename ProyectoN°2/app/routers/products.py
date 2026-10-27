from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from database import Session
from Modelos import Product
from schemas import Product_activate, Product_create, ProductUpdate

router = APIRouter(prefix="/products", tags=["Productos"])
@router.get("", status_code= 200) #lista de productos
def listar_product(category_id: Optional[int] = Query(None, description="Filtrar por id de categorya"), available: bool = Query(False, description="Si esta true, retorna solo producto disponibles") ): # optional , query escribir lo que hace el optional y query
    with Session() as session:
        query = select(Product)

        if available is not None:
            query = query.where(Product.availability == True)

        if category_id is not None:
            query = query.where(Product.category_id == category_id)

        product = session.execute(query).scalars().all()
        return  product

@router.get("/{id}", status_code=200) #busqueda por id del producto
def busqueda_id_product(id: int):
    with Session() as session:
        product = session.get(Product, id)
        if product is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return product

@router.post("",status_code= 201) #crear producto
def insert_product(producto: Product_create):
    with Session() as session:
        NewProduct = Product(**producto.model_dump()) # seguramente hacer que no se repitan los productos preguntar a la profe
        session.add(NewProduct)
        session.commit()
        session.refresh(NewProduct)
        return NewProduct

@router.put("/{id}", status_code=200)
def actualizarProducto(id: int, datos: ProductUpdate):
    with Session() as session:
        producto = session.get(Product, id)
        if not producto: 
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        dict_act = datos.model_dump(exclude_unset=True)
        for clave, valor in dict_act.items():
            setattr(producto, clave, valor)

        session.commit()
        session.refresh(producto)
        return producto

@router.post("/{product_id}/activate",status_code = 200)
def activate_false(product_id: int, act: Product_activate):
    with Session() as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        if act.availability and product.stock <= 0:
            raise HTTPException(status_code=400, detail="No se puedo activar el producto porque no tiene stock")

        product.availability = act.availability
        session.commit()
        session.refresh(product)
        return{"mensaje": "Estado actualizado", "ID Producto": product.id, "Estado": product.availability, "Stock": product.stock}
