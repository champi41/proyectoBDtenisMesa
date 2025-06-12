import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

# WARN: No uses credenciales en producción sin variables de entorno
# URI: "postgresql://user:password@localhost:port/dbname"
DATABASE_URI = os.getenv("DATABASE_URI", "")
engine = create_engine(DATABASE_URI)
metadata = MetaData(schema=os.getenv("DATABASE_SCHEMA", "public"))
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base(metadata=metadata)