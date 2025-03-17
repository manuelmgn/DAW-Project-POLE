"""
Funcións auxiliares para a xestión de usuarios.
Diferénciase de users/utils.py en que esta contén funcións son requeridas pola
base de datos para evitar a creación de bucles de importación.
"""

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from users.models import User
from user_logs.models import UserLog

# ==============================================================================
# VERIFICACIÓNS
# ==============================================================================

# ------------------------------------------------------------------------------
# VERIFICAR USUARIO EXISTENTE
# ------------------------------------------------------------------------------


def verify_existing_user(id, db: Session = Depends(get_db)):
    """
    Verificar se existe un usuario, dado o seu ID.

    Args:
        id (int): ID do usuario.
        db (Session): Sesión da base de datos.

    Raises:
        HTTPException: Se non se encontra ningún usuario co ID dado.
    """

    existing_user = db.query(User).filter(User.id_user == id).first()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontrou ningún usuario co id {id}",
        )


# ==============================================================================
# GETTING INFO
# ==============================================================================

# ------------------------------------------------------------------------------
# USER DEFAULT LOCATION
# ------------------------------------------------------------------------------


def get_user_location(user_id, db: Session = Depends(get_db)):
    """
    Obter a localización por defecto dun usuario.

    Args:
        user_id (int): ID do usuario.
        db (Session): Sesión da base de datos.

    Returns:
        dict: Localización do usuario.

    Raises:
        HTTPException: Se non se encontra ningún usuario co ID dado.
        HTTPException: Se o usuario non ten marcada unha localización.
    """

    db_user = db.query(User).filter(User.id_user == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario non encontrado")
    if db_user.location is None:
        raise HTTPException(
            status_code=404,
            detail="O usuario non ten marcada unha localización",
        )

    return db_user.location


# ------------------------------------------------------------------------------
# USER LOGS
# ------------------------------------------------------------------------------


def get_user_logs(user_id, db: Session = Depends(get_db)):
    """
    Obter os rexistros dun usuario.

    Args:
        user_id (int): ID do usuario.
        db (Session): Sesión da base de datos.

    Returns:
        List[UserLog]: Lista de rexistros do usuario.

    Raises:
        HTTPException: Se non se encontra ningún usuario co ID dado.
        HTTPException: Se o usuario non ten rexistros.
    """

    db_user = db.query(User).filter(User.id_user == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario non encontrado")

    user_logs = db.query(UserLog).filter(UserLog.user_id == user_id).all()

    if user_logs is None:
        raise HTTPException(
            status_code=404, detail="O usuario non ten rexistros"
        )

    return user_logs
