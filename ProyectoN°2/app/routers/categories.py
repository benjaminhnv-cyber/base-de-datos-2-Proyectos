from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import Session
from Modelos import Category
from schemas import Catagory_create


router = APIRouter(prefix="/category", tags=["Category"])

@router.get("",status_code=200)
def listar_category():
    with Session() as session:
        category = session.execute(select(Category)).scalars().all()
        return category

@router.post("",status_code= 201)
def insert_category(category: Catagory_create):
    with Session() as session:
        categoria_existente = session.execute(select(Category).where(Category.name == category.name)).scalar_one_or_none()
        if categoria_existente:
            raise HTTPException(status_code=400, detail=f"La categoría '{category.name}' ya existe.")
        
        new_category = Category(**category.model_dump())
        session.add(new_category)
        session.commit()
        session.refresh(new_category)
        return new_category

@router.delete("/{id}",status_code=200)
def delate_category(id:int):
    with Session() as session:
        category = session.get(Category, id)
        if not category:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        if len(category.products) > 0:
            raise HTTPException(status_code=400, detail="No se puede eliminar la categoría porque tiene productos asociados.")
            
        session.delete(category)
        session.commit()
        return {"mensaje": "Categoría eliminada exitosamente"}