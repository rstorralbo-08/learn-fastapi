from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import FastAPI, APIRouter, Depends, Response, status
from database import Base, engine
from database import get_db
from schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResposta
from models.produtos import Produto as ProdutoModel  # Modelo do SQLAlchemy
#from app.services.produto_service import ProdutoService
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Produtos",
    description="API CRUD usando FastAPI, SQLAlchemy e MySQL",
    version="1.0.0",
)

produtos = [
    {
        "id": 1,
        "descricao": "Notebook",
        "preco": 3500.00
    },
    {
        "id": 2,
        "descricao": "Mouse",
        "preco": 80.00
    }
]

class Produto(BaseModel):
    descricao: str
    preco: float

@app.get("/")
def inicio():
    return {"mensagem": "API de Produtos funcionando"}

@app.get("/produtos", response_model=list[ProdutoResposta])
def listar_produtos(db: Session = Depends(get_db)):
    stmt = select(ProdutoModel).order_by(ProdutoModel.id)
    produtos = db.scalars(stmt).all()
    return produtos

@app.get("/produtos/{id}", response_model=ProdutoResposta)
def buscar_produto(id: int, db: Session = Depends(get_db)):
    # Busca o produto no banco de dados pelo ID
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
    
    # Se não encontrar, retorna um erro 404 padronizado do FastAPI
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
        
    return produto

@app.post("/produtos", response_model=ProdutoResposta, status_code=201)
def cadastrar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    # Cria uma instância do MODELO DO SQLAlchemy usando os dados validados do Pydantic
    produto = ProdutoModel(**dados.model_dump())
    
    db.add(produto)
    db.commit()
    db.refresh(produto)
    
    return produto

@app.put("/produtos/{id}", response_model=ProdutoResposta)
def atualizar_produto(id: int, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    # 1. Busca o produto no banco pelo ID
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
    
    # 2. Se não encontrar, retorna erro 404
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # 3. Pega apenas os campos que foram enviados na requisição
    dados_atualizados = dados.model_dump(exclude_unset=True)
    
    # 4. Atualiza dinamicamente os atributos do produto no banco
    for campo, valor in dados_atualizados.items():
        setattr(produto, campo, valor)
        
    db.commit()
    db.refresh(produto)
    
    return produto

@app.delete("/produtos/{id}", status_code=204)
def deletar_produto(id: int, db: Session = Depends(get_db)):
    # 1. Busca o produto no banco pelo ID
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == id).first()
    
    # 2. Se não encontrar, retorna erro 404
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # 3. Deleta o registro do banco
    db.delete(produto)
    db.commit()
    
    # Por padrão, requisições DELETE bem-sucedidas retornam status 204 (No Content) sem corpo de resposta
    return None