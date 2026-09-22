from pydantic import BaseModel, EmailStr, Field

class UsuarioCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    edad: int = Field(..., gt=0, lt=120)
    password: str = Field(..., min_length=6, description="Contraseña segura de al menos 6 caracteres")

class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    edad: int

    class Config:
        from_attributes = True  # Permite mapear modelos de SQLAlchemy directamente