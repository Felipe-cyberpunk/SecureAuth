import re
from pydantic import BaseModel, EmailStr, Field, field_validator

class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    edad: int = Field(..., ge=18, le=120)
    password: str = Field(..., min_length=6)

    @field_validator('username')
    def validar_caracteres_username(cls, v):
        # Bloquea caracteres especiales extraños o intentos de inyección a nivel de entrada
        if not re.match("^[a-zA-Z0-9_]+$", v):
            raise ValueError("El nombre de usuario solo debe contener letras, números y guiones bajos.")
        return v

class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    edad: int

    class Config:
        from_attributes = True  # Permite mapear modelos de SQLAlchemy directamente
        
@field_validator('password')
def validar_complexidad_password(cls, v):
    if len(v) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r"[A-Z]", v):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r"[a-z]", v):
        raise ValueError("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r"[0-9]", v):
        raise ValueError("La contraseña debe contener al menos un número.")
    return v        