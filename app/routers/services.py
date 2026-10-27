from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import database, models, schemas

router = APIRouter(prefix="/services", tags=["Servicios (Catálogo)"])

@router.post("/", response_model=schemas.ServiceResponse, status_code=201)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(database.get_db)):
    """Registra un nuevo estilo de corte en el catálogo."""
    new_service = models.Service(**service.model_dump())
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@router.get("/", response_model=List[schemas.ServiceResponse])
def get_services(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """Devuelve la lista de servicios/cortes disponibles."""
    services = db.query(models.Service).offset(skip).limit(limit).all()
    return services

@router.get("/{service_id}", response_model=schemas.ServiceResponse)
def get_service(service_id: int, db: Session = Depends(database.get_db)):
    """Obtiene los detalles de un servicio específico por su ID."""
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return db_service

@router.put("/{service_id}", response_model=schemas.ServiceResponse)
def update_service(service_id: int, service_update: schemas.ServiceUpdate, db: Session = Depends(database.get_db)):
    """Actualiza campos específicos (como precio o duración) de un servicio."""
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
        
    update_data = service_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
        
    db.commit()
    db.refresh(db_service)
    return db_service

@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(database.get_db)):
    """Elimina físicamente un servicio del catálogo."""
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
        
    db.delete(db_service)
    db.commit()
    return {"message": "Servicio eliminado del catálogo exitosamente"}