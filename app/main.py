from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routers import auth, users, services, products

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SmartCut AI API",
    description="API REST para la gestión de SmartCut AI",
    version="1.0.0"
)

# Configuración de orígenes permitidos (CORS):
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5501",
        "http://127.0.0.1:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(services.router)
app.include_router(products.router)


@app.get("/", tags=["Raíz"])
def root():
    return {
        "mensaje": "¡Bienvenido a la API de SmartCut AI!",
        "docs_url": "/docs",
        "estado": "Operativa"
    }