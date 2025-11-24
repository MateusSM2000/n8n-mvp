from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..database import get_db
from .. import models, schemas
from typing import List
from pydantic import HttpUrl
from enum import Enum

router = APIRouter(prefix="/personalizados", tags=["Pedidos Personalizados"])


@router.post("/", response_model=schemas.pedido_personalizado.PedidoPersonalizado, status_code=status.HTTP_201_CREATED)
def criar_pedido(pedido: schemas.pedido_personalizado.PedidoPersonalizadoCreate, db: Session = Depends(get_db)):
    novo = models.pedido_personalizado.PedidoPersonalizado(
        telefone_cliente=pedido.telefone_cliente,
        tipo_produto=pedido.tipo_produto,
        tema=pedido.tema,
        instrucoes=pedido.instrucoes,
        urls_imagens_sugeridas=[]
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/", response_model=List[schemas.pedido_personalizado.PedidoPersonalizado])
def listar_pedidos(status: schemas.pedido_personalizado.StatusPedido | None = None, db: Session = Depends(get_db)):
    q = db.query(models.pedido_personalizado.PedidoPersonalizado)
    if status:
        q = q.filter(models.pedido_personalizado.PedidoPersonalizado.status == status.value)
    return q.order_by(models.pedido_personalizado.PedidoPersonalizado.criado_em.desc()).all()

@router.get("/{pedido_id}", response_model=schemas.pedido_personalizado.PedidoPersonalizado)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    p = db.query(models.pedido_personalizado.PedidoPersonalizado).filter(models.pedido_personalizado.PedidoPersonalizado.id == pedido_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return p

@router.put("/{pedido_id}", response_model=schemas.pedido_personalizado.PedidoPersonalizado)
def atualizar_pedido(pedido_id: int, update: schemas.pedido_personalizado.PedidoPersonalizadoUpdate, db: Session = Depends(get_db)):
    p = db.query(models.pedido_personalizado.PedidoPersonalizado).filter(models.pedido_personalizado.PedidoPersonalizado.id == pedido_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    p.status = update.status.value
    db.commit()
    db.refresh(p)
    return p

@router.post("/{pedido_id}/imagens", response_model=schemas.pedido_personalizado.PedidoPersonalizado)
def adicionar_imagens(pedido_id: int, imagens: List[HttpUrl], db: Session = Depends(get_db)):
    p = db.query(models.pedido_personalizado.PedidoPersonalizado).filter(models.pedido_personalizado.PedidoPersonalizado.id == pedido_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    p.urls_imagens_sugeridas = imagens
    db.commit()
    db.refresh(p)
    return p