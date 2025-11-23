from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from assistente_grafica_api.app.database import SessionLocal
from assistente_grafica_api.app.database import get_db
from assistente_grafica_api.app import models, schemas

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/", response_model=schemas.categoria.Categoria, status_code=status.HTTP_201_CREATED)
def criar_categoria(cat: schemas.categoria.CategoriaCreate, db: Session = Depends(get_db)):
    # impedir duplicada
    existe = db.query(models.categoria.Categoria).filter(models.categoria.Categoria.nome == cat.nome).first()
    if existe:
        raise HTTPException(status_code=400, detail="Categoria já existe.")

    nova = models.categoria.Categoria(nome=cat.nome)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.get("/", response_model=list[schemas.categoria.Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(models.categoria.Categoria).all()


@router.get("/{categoria_id}", response_model=schemas.categoria.Categoria)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    c = db.query(models.categoria.Categoria).filter(models.categoria.Categoria.id == categoria_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")
    return c


@router.put("/{categoria_id}", response_model=schemas.categoria.Categoria)
def atualizar_categoria(categoria_id: int, cat: schemas.categoria.CategoriaCreate, db: Session = Depends(get_db)):
    c = db.query(models.categoria.Categoria).filter(models.categoria.Categoria.id == categoria_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")

    c.nome = cat.nome
    db.commit()
    db.refresh(c)
    return c


@router.delete("/{categoria_id}", status_code=204)
def deletar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    c = db.query(models.categoria.Categoria).filter(models.categoria.Categoria.id == categoria_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Categoria não encontrada.")

    db.delete(c)
    db.commit()