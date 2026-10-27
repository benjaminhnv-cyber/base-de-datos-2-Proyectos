from decimal import Decimal
from database import Session, engine
from Modelos import Base, Category, Product, Table

def cargar_datos_iniciales():
    Base.metadata.create_all(engine)    
    with Session() as session:
        if session.query(Category).count() > 0:
            print("La base de datos ya contiene información inicial.")
            return

        print("Insertando datos iniciales...")
        cat_entradas = Category(name="Entradas", description="Platos para compartir")
        cat_fondos = Category(name="Platos de Fondo", description="Platos principales")
        cat_bebidas = Category(name="Bebidas", description="Jugos y refrescos")
        
        session.add_all([cat_entradas, cat_fondos, cat_bebidas])
        session.flush()

        prod1 = Product(name="Empanadas de Pino", description="2 unidades tradicionales", price=Decimal("3500.00"), stock=20, availability=True, category_id=cat_entradas.id)
        prod2 = Product(name="Lomo a lo Pobre", description="Lomo con papas fritas y huevo", price=Decimal("12500.00"), stock=3, availability=True, category_id=cat_fondos.id)
        prod3 = Product(name="Jugo Natural de Frambuesa", description="Vaso 500ml", price=Decimal("2800.00"), stock=1, availability=True, category_id=cat_bebidas.id)

        session.add_all([prod1, prod2, prod3])

        mesa1 = Table(number=1, capacity=2, availability=True)
        mesa2 = Table(number=2, capacity=4, availability=True)
        mesa3 = Table(number=3, capacity=6, availability=True)

        session.add_all([mesa1, mesa2, mesa3])
        session.commit()
        print("¡Datos de prueba cargados exitosamente!")


if __name__ == "__main__":
    cargar_datos_iniciales()