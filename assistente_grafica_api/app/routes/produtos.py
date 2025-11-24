from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models.produto import Produto
from ..models.categoria import Categoria
from ..schemas.produto import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse
)

router = APIRouter(prefix="/produtos", tags=["Produtos"])


# ----------------------------------------------------------
# GET ALL + filtros
# ----------------------------------------------------------
@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(
    db: Session = Depends(get_db),
    nome: Optional[str] = Query(None, min_length=2),
    categoria_id: Optional[int] = None,
    ativo: Optional[bool] = True
):
    query = db.query(Produto)

    if nome:
        query = query.filter(Produto.nome.like(f"%{nome}%"))

    if categoria_id:
        query = query.filter(Produto.categoria_id == categoria_id)

    if ativo is not None:
        query = query.filter(Produto.ativo == ativo)

    return query.all()


# ----------------------------------------------------------
# GET BY ID
# ----------------------------------------------------------
@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


# ----------------------------------------------------------
# CREATE
# ----------------------------------------------------------
@router.post("/", response_model=ProdutoResponse, status_code=201)
def criar_produto(payload: ProdutoCreate, db: Session = Depends(get_db)):

    categoria = db.query(Categoria).filter(Categoria.id == payload.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    produto = Produto(**payload.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


# ----------------------------------------------------------
# UPDATE
# ----------------------------------------------------------
@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, payload: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if payload.categoria_id:
        categoria = db.query(Categoria).filter(Categoria.id == payload.categoria_id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria inválida")

    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)
    return produto


# ----------------------------------------------------------
# DELETE (soft-delete)
# ----------------------------------------------------------
@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto.ativo = False
    db.commit()
    return {"mensagem": "Produto desativado com sucesso"}