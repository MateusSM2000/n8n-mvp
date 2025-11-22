from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from assistente_grafica_api.app.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)

    produtos = relationship("Produto", back_populates="categoria")