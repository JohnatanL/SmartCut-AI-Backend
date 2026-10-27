from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app import database, models, schemas, security

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Autentica al usuario verificando su hash y devuelve un JWT."""
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify", response_model=schemas.UserResponse)
def verify_token(current_user: models.User = Depends(security.get_current_user)):
    """Verifica que el JWT provisto sea válido y devuelve la información del usuario autenticado."""
    return current_user

@router.put("/update-password")
def update_password(password_data: schemas.PasswordUpdate, current_user: models.User = Depends(security.get_current_user), db: Session = Depends(database.get_db)):
    """Actualiza la contraseña del usuario actualmente autenticado."""
    hashed_pwd = security.get_password_hash(password_data.new_password)
    current_user.hashed_password = hashed_pwd
    db.commit()
    return {"message": "Contraseña actualizada exitosamente"}

@router.delete("/logout")
def logout(current_user: models.User = Depends(security.get_current_user)):
    """
    Simula el cierre de sesión. 
    Nota técnica: Al usar JWT stateless, no existe estado en el servidor. 
    Este endpoint notifica éxito, pero el cliente (Frontend) DEBE eliminar 
    físicamente el token de su LocalStorage/Memoria para que el logout sea efectivo.
    """
    return {"message": "Cierre de sesión exitoso. Por favor, elimine el token en el cliente."}