# infrastructure/models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"  # Este es el nombre exacto de la tabla que creaste en SQL Server

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    edad = Column(Integer, nullable=False)