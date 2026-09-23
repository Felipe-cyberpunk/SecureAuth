import os
import uuid
from datetime import datetime, timedelta
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from infrastructure.models import AuditLogModel, UsuarioModel
from infrastructure.database import SessionLocal, get_db

# 1. Configuración de seguridad (Variables globales primero)
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_super_segura_por_defecto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

# Configuramos el contexto de encriptación con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    """Toma una contraseña en texto plano y retorna su hash seguro."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)

# 2. Función única para crear el token incluyendo el JTI (Sesión única)
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> tuple[str, str]:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    # Generamos un ID de sesión único (jti)
    jti = str(uuid.uuid4())
    
    to_encode.update({"exp": expire, "jti": jti})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt, jti

# 3. Función get_current_user validando Cookies HttpOnly y JTI en Base de Datos
def get_current_user(request: Request) -> str:
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se encontró el token de sesión en las Cookies"
        )
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o la sesión expiró/fue reemplazada",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_jti: str = payload.get("jti")
        
        if username is None or token_jti is None:
            raise credentials_exception
            
        # Abrimos una sesión rápida a la BD para validar el JTI activo
        db: Session = SessionLocal()
        try:
            user = db.query(UsuarioModel).filter(UsuarioModel.username == username).first()
            if not user or user.token_jti != token_jti:
                # Si el JTI no coincide, la sesión fue reemplazada en otro inicio de sesión
                raise credentials_exception
        finally:
            db.close()
            
    except JWTError:
        raise credentials_exception
    
    return username

def get_admin_user(
    current_username: str = Depends(get_current_user),
    db: Session = Depends(get_db)):
    
    user = db.query(UsuarioModel).filter(UsuarioModel.username == current_username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado."
        )
    
    # Validamos si su rol es administrador
    if user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren privilegios de Administrador."
        )
        
    return user

def registrar_auditoria(db: Session, username: str, accion: str, request: Request = None):
    # Corregido: request.client en lugar de request.cliente
    client_ip = request.client.host if request and request.client else "Desconocida"
    
    nuevo_log = AuditLogModel(
        username=username,
        accion=accion,
        ip_address=client_ip
    )
    db.add(nuevo_log)
    db.commit()