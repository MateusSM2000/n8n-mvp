from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from assistente_grafica_api.app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    preco = Column(DECIMAL(10,2))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    url_imagem = Column(String(500))
    tem_estoque = Column(Boolean, default=True)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    categoria = relationship("Categoria", back_populates="produtos")