from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return "¡Hola Mundo!"

@app.get("/url_test")
async def url():
    return { "url_curso": "https://sofi.com.diego" }