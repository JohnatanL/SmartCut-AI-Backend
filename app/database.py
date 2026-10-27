from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Se utilizará SQLite. La base de datos se guardará en la carpeta /data (persistida por Docker)
os.makedirs("data", exist_ok=True)
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/smartcut.db"

# engine es la interfaz de conexión a la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal se usará para crear instancias de conexión por cada petición
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base sirve como clase padre para que SQLAlchemy mapee nuestras clases a tablas
Base = declarative_base()

def get_db():
    """
    Genera una sesión de base de datos para una petición HTTP
    y la cierra automáticamente al terminar.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()