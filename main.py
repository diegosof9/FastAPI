from fastapi import FastAPI
from routers import products, users


app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return "¡Hola Mundo!"


@app.get("/url_test")
async def url():
    return { "url_curso": "https://sofi.com.diego" }