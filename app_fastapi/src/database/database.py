"""Conexión coa base de datos"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from users.utils import load_admin
from pollens.utils import load_pollen_types

DATABASE_URL = (
    os.getenv("DATABASE_URL")
    or "postgresql://a22manuelma:password@172.18.0.2:5432/poledb"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Función para conectarse á base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicia a base de datos
    """
    from database.base import Base

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Carga os tipos de pole
        load_pollen_types(db)
        # Carga o usuario administrador
        load_admin(db)
    finally:
        db.close()
