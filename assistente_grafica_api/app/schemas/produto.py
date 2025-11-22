from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional, List
from decimal import Decimal


# ----------------------------------------------------------
# Base (campos comuns)
# ----------------------------------------------------------
class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=120)
    descricao: Optional[str] = Field(None, max_length=2000)
    preco: Decimal = Field(..., gt=0)
    categoria_id: int = Field(...)
    imagens: Optional[List[HttpUrl]] = []
    ativo: bool = True

    @field_validator("nome")
    def limpar_nome(cls, v):
        return " ".join(v.split())

    @field_validator("descricao")
    def limpar_descricao(cls, v):
        return " ".join(v.split()) if v else v


# ----------------------------------------------------------
# Create
# ----------------------------------------------------------
class ProdutoCreate(ProdutoBase):
    pass


# ----------------------------------------------------------
# Update (todos opcionais)
# ----------------------------------------------------------
class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=2, max_length=120)
    descricao: Optional[str] = Field(None, max_length=2000)
    preco: Optional[Decimal] = Field(None, gt=0)
    categoria_id: Optional[int]
    imagens: Optional[List[HttpUrl]]
    ativo: Optional[bool]

    @field_validator("nome")
    def limpar_nome(cls, v):
        return " ".join(v.split()) if v else v

    @field_validator("descricao")
    def limpar_descricao(cls, v):
        return " ".join(v.split()) if v else v


# ----------------------------------------------------------
# Response (com ID)
# ----------------------------------------------------------
class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        orm_mode = True