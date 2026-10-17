from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    descricao: Mapped[str] = mapped_column(String(150), nullable=False)
    preco: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    estoque: Mapped[int] = mapped_column(Integer, nullable=False, default=0)