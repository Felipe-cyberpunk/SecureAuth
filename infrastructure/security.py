import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

#Configuracion de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_super_segura_por_defecto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 


#configuramos el contexto de encriptación con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str)-> bool:
    """Verifica si una contraseña en texto plano Coincide con su hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str)-> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#Función de despendencia que valida el token

def get_current_user(token: str = Depends(oauth2_scheme))-> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    
    try:
        pauload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        username: str = pauload.get("sub")
        
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    return username    

def hash_password(password: str) -> str:
    """toma una contraseña en texto plano u retonra su has seguro."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)-> bool:
    """verifica si la congraseña en texto plano coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)
