from sqlalchemy import Column, Integer, String, Text, JSON, Enum, DateTime
from sqlalchemy.sql import func
from assistente_grafica_api.app.database import Base

class PedidoPersonalizado(Base):
    __tablename__ = "pedidos_personalizados"

    id = Column(Integer, primary_key=True)
    telefone_cliente = Column(String(20))
    tipo_produto = Column(String(255))
    tema = Column(Text)
    instrucoes = Column(Text)
    urls_imagens_sugeridas = Column(JSON)
    status = Column(Enum("aberto", "em_andamento", "concluido"), default="aberto")
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())