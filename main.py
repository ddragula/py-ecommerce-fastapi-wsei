from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.database import engine
from api import models
from api.routers import auth, products, basket, orders

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce Platform",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(basket.router)
app.include_router(orders.router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
