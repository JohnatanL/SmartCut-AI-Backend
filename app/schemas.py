from pydantic import BaseModel, EmailStr
from typing import Optional

# ==========================================
# SCHEMAS DE USUARIO (Demostrando Herencia)
# ==========================================
class UserBase(BaseModel):
    email: EmailStr
    nombre: str

class UserCreate(UserBase):
    password: str # Se requiere password para crearlo

class UserUpdate(BaseModel):
    # Campos opcionales para actualizar
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    # No incluimos password aquí por seguridad
    class Config:
        from_attributes = True

# ==========================================
# SCHEMAS DE SERVICIOS (Catálogo)
# ==========================================
class ServiceBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    duracion_minutos: int

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    duracion_minutos: Optional[int] = None

class ServiceResponse(ServiceBase):
    id: int
    class Config:
        from_attributes = True

# ==========================================
# SCHEMAS DE PRODUCTOS (Inventario)
# ==========================================
class ProductBase(BaseModel):
    nombre: str
    marca: str
    precio: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    nombre: Optional[str] = None
    marca: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

# ==========================================
# SCHEMAS DE AUTENTICACIÓN
# ==========================================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class PasswordUpdate(BaseModel):
    new_password: str