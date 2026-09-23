import uuid
import pyodbc
from datetime import timedelta
from infrastructure.models import AuditLogModel, UsuarioModel
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from infrastructure.security import get_admin_user, get_current_user, registrar_auditoria
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from infrastructure.security import (
    create_access_token, 
    verify_password, 
    hash_password, 
    SECRET_KEY, 
    ALGORITHM
)
from infrastructure.database import SessionLocal, engine, Base, get_db
from schema.usuario_schema import UsuarioCreate, UsuarioResponse

# Creamos la tabla en la DB si no existe
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SecureAuth API",
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter  # Corregido: instancia en minúscula
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(pyodbc.Error)
async def database_exception_handler(request: Request, exc: pyodbc.Error):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Database Unavailable",
            "mensaje": "El servicio de base de datos no esta disponible temporalmente"
        }
    )

@app.exception_handler(Exception)
async def gloabl_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "mensaje": "Ocurrio un error inesperado procesando su solicitud."
        }
    )

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31436000; includeSubDomains; preload"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "Strict-origin-when-cross-origin"
    return response    

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a SecureAuth Backend - Conectando a docker y Operativo"}

@app.post("/token")
@limiter.limit("5/minute")
def login_para_obtener_token(request: Request, response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UsuarioModel).filter(UsuarioModel.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o contraseña incorrectos"
        )
        
    access_token_expires = timedelta(minutes=30)
    access_token, session_jti = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires  
    )
    
    user.token_jti = session_jti
    db.commit()
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  
        samesite="lax",
        max_age=1800
    )
    
    return {"mensaje": "Inicio de sesión exitoso. Sesión única asegurada."}

@app.get("/usuarios/me", tags=["seguridad"])
def leer_usuario_actual(current_user: str = Depends(get_current_user)):
    return {"usuario": current_user, "estado": "Acceso autorizado de forma segura"}

@app.post("/usuarios/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    
    hashed_pass = hash_password(usuario.password)
    nuevo_usuario = UsuarioModel(
        username=usuario.username,
        email=usuario.email,
        edad=usuario.edad,
        password_hash=hashed_pass
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.get("/usuarios/", response_model=list[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioModel).order_by(UsuarioModel.id).offset(skip).limit(limit).all()
    return usuarios

@app.post("/logout")
def logout(response: Response, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(UsuarioModel).filter(UsuarioModel.username == current_user).first()
    
    if user:
        user.token_jti = None
        db.commit()
        
    response.delete_cookie(key="access_token") # Corregido: uso de la instancia response
    
    return {"mensaje": "Sesión cerrada exitosamente. Token invalidado."}

@app.get("/perfil")
def ver_perfil(current_user: str = Depends(get_current_user)):
    return {"mensaje": f"Hola {current_user}, esta es tu zona personal. "}

@app.get("/admin/dashboard-secreto")
def panel_de_control_admin(
    request: Request,
    admin_user: UsuarioModel = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    registrar_auditoria(db, username=admin_user.username, accion="ACCESO_PANEL_ADMIN", request=request)
    
    return {
        "estado": "Acceso concedido",
        "mensaje": f"Bienvenido, Administrador: {admin_user.username}"
    }
    
@app.get("/admin/audit-logs")
def consultar_logs_auditoria(
    admin_user: UsuarioModel = Depends(get_admin_user),
    db: Session = Depends(get_db)):
    
    logs = db.query(AuditLogModel).order_by(AuditLogModel.timestamp.desc()).limit(50).all()
    
    return {
        "mensaje": "Historial forense de seguridad obtenido con éxito",
        "total_registros": len(logs),
        "registros": [
            {
                "id": log.id,
                "usuario": log.username,
                "accion": log.accion,
                "ip": log.ip_address,
                "fecha_hora": log.timestamp
            }
            for log in logs
        ]
    }