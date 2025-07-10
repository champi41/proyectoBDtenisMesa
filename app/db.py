import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# WARN: No uses credenciales en producción sin variables de entorno
# URI: "postgresql://user:password@localhost:port/dbname"
DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://user:password@localhost:5432/your_db_name") 
engine = create_engine(DATABASE_URI)
metadata = MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() 

def get_db():
    """
    Función para obtener una sesión de base de datos que se puede usar en tus rutas/funciones.
    Asegura que la sesión se cierre correctamente después de su uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
