from pydantic import BaseModel, Field

class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=2)

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        orm_mode = True