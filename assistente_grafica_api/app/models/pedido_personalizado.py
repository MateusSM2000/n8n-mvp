from sqlalchemy import Column, Integer, String, Text, JSON, Enum as SAEnum, DateTime
from sqlalchemy.sql import func
from ..database import Base
from enum import Enum

class StatusPedido(str, Enum):
    aberto = "aberto"
    em_andamento = "em_andamento"
    concluido = "concluido"

class PedidoPersonalizado(Base):
    __tablename__ = "pedidos_personalizados"

    id = Column(Integer, primary_key=True)
    telefone_cliente = Column(String(20))
    tipo_produto = Column(String(255))
    tema = Column(Text)
    instrucoes = Column(Text)
    urls_imagens_sugeridas = Column(JSON)
    status = Column(SAEnum(StatusPedido), default=StatusPedido.aberto)
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())