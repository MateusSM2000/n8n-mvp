from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from enum import Enum

class StatusPedido(str, Enum):
    aberto = "aberto"
    em_andamento = "em_andamento"
    concluido = "concluido"

class PedidoPersonalizadoBase(BaseModel):
    telefone_cliente: Optional[str] = Field(None, min_length=8, max_length=20)
    tipo_produto: Optional[str] = Field(None, max_length=255)
    tema: Optional[str]
    instrucoes: Optional[str]

class PedidoPersonalizadoCreate(PedidoPersonalizadoBase):
    pass

class PedidoPersonalizadoUpdate(BaseModel):
    status: StatusPedido

class PedidoPersonalizado(PedidoPersonalizadoBase):
    id: int
    urls_imagens_sugeridas: Optional[List[HttpUrl]] = []
    status: StatusPedido

    class Config:
        orm_mode = True