from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import Session
from Modelos import Table
from schemas import Table_create, Table_update

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.get("",status_code=200)
def listar_tables():
    with Session() as session:
        tables = session.execute(select(Table)).scalars().all()
        return tables

@router.get("/{number}",status_code=200)
def obtener_number(number: int):
    with Session() as session:
        table = session.execute(select(Table).where(Table.number == number)).scalar_one_or_none()
        if not table:
            raise HTTPException(status_code=404, detail = "Mesa no encontrada")
        return table

@router.post("",status_code=201)
def insert_tables(tab: Table_create):
    with Session() as session:
        mesa_existente = session.execute(select(Table).where(Table.number == tab.number)).scalar_one_or_none()
        if mesa_existente:
            raise HTTPException(status_code=400,detail=f"La mesa número {tab.number} ya existe")
        
        new_table = Table(**tab.model_dump())
        session.add(new_table)
        session.commit()
        session.refresh(new_table)
        return new_table

@router.patch("/{number}", status_code=200) # cambiar no esta completa 8899
def actualizar_table(number: int, data_actualizar: Table_update):
    with Session() as session:
        table = session.execute(select(Table).where(Table.number == number)).scalar_one_or_none()
        if not table:
            raise HTTPException(status_code=404, detail="Mesa no encontrada")
        
        dict_act = data_actualizar.model_dump(exclude_unset=True)
        for clave, valor in dict_act.items():
            setattr(table, clave, valor)
            
        session.commit()
        session.refresh(table)
        return table