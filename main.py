from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from infrastructure.security import create_access_token, get_current_user, verify_password
from sqlalchemy.orm import Session
from infrastructure.database import SessionLocal, engine, Base
from infrastructure.models import UsuarioModel
from infrastructure.security import hash_password
from schema.usuario_schema import UsuarioCreate, UsuarioResponse


#Creamos la tabla en la DB si no ExtendedInterpolation
Base.metadata.create_all(bind=engine)
USUARIO_REGISTRADO = "admin"
HASH_CONTRASENA_GUARDADA = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
app = FastAPI(
    title="SecureAuth API",
)


@app.post("/token")
def login_para_obtener_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != USUARIO_REGISTRADO: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Usuario o contraseña incorrectas"
        )
        
    if not verify_password(form_data.password, HASH_CONTRASENA_GUARDADA):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o contraseña incorrectos"
        )    
        
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires  
    )
    
    return {"access_token": access_token, "token_type": "bearer"}



@app.get("/usuarios/me", tags=["seguridad"])
def leer_usuario_actual(current_user: str = Depends(get_current_user)):
    return {"usuario": current_user, "estado": "Acceso autorizado de forma segura"}
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.get("/")
def read_root():
    return{"mensaje": "Bienvenido a SecureAuth Backend - Conectando a docker y Operativo"}

@app.post("/usuarios/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="el correo electronico ya está registrado")
    
    
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
            