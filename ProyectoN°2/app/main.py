from fastapi import FastAPI
from routers import categories, products, tables, orders, reports


app = FastAPI(
    title="API Restaurante",
    description="Sistema de gestión de carta, mesas, pedidos y reportes",
    version="1.0.0"
)

# Inclusión de Routers / tienes que modificar los archivos ya hice orders
app.get("/")
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(tables.router)
app.include_router(orders.router)
app.include_router(reports.router)
#este aqui hay unr error que me da palo hacer base de datos e¿problemas que no funcion ub unicorn de alogo apirouter