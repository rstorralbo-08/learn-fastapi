from pydantic import BaseModel, ConfigDict, Field

class ProdutoBase(BaseModel):
    descricao: str = Field(min_length=2, max_length=150)
    preco: float = Field(gt=0)
    estoque: int = Field(ge=0)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    pass

class ProdutoResposta(ProdutoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)