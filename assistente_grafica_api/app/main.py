from fastapi import FastAPI
from routes import produtos, categorias, personalizados
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(produtos.router)
app.include_router(categorias.router)
app.include_router(personalizados.router)

@app.get("/")
def root():
    return {"status": "API da gráfica rodando!"}