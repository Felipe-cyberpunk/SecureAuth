# infrastructure/models.py
from sqlalchemy import Column, Integer, String, DateTime, func
from infrastructure.database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    edad = Column(Integer, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    token_jti = Column(String(36), nullable=True)
    
    rol = Column(String(20), default="user", nullable=False)
    
    
class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), nullable=False)          # Quién realizó la acción
    accion = Column(String(255), nullable=False)           # Qué hizo (ej. "LOGIN_EXITOSO", "INTENTO_ACCESO_ADMIN")
    ip_address = Column(String(50), nullable=True)         # Desde qué IP lo hizo
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) # Cuándo lo hizo (automático)    