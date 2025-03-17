"""Funcións útiles para xestionar os tipos de pole"""

from typing import List
from sqlalchemy.orm import Session

from .models import PollenType, Pollen


def get_all_pollen_types() -> List[str]:
    """
    Devolve os tipos de pole.

    Returns:
        List[str]: Lista cos nomes dos tipos de pole.
    """

    return [pollen.value for pollen in PollenType]


def load_pollen_types(db: Session):
    """
    Carga os tipos de pole na base de datos.

    Args:
        db (Session): Sesión da base de datos.

    Returns:
        Nada
    """
    try:
        # Verificar se a táboa está baleira
        existing_pollens = db.query(Pollen).count()

        if existing_pollens == 0:
            for pollen_type in PollenType:
                pollen = Pollen(
                    pollen_name=pollen_type.name, pollen_gal=pollen_type.value
                )
                db.add(pollen)
            print("Tipos de pole cargadas na base de datos")
            db.commit()

    except Exception as e:
        print("Erro ao cargar os tipos de pole na BD:", str(e))
        db.rollback()

    finally:
        db.close()
