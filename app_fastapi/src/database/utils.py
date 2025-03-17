"""Funcións útiles para o manexo da base de datos"""

from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import Depends
from passlib.context import CryptContext

from user_logs.models import UserLog
from database.database import get_db
from database.relations import UserPollens
from users.models import User


# ==============================================================================
# FUNCIÓNS DE TÁBOAS INTERMEDIAS
# ==============================================================================


def delete_user_pollens(user_id, db: Session):
    """
    Elimina todas as filas de user_pollens dun usuario, dado o seu ID

    Args:
        user_id (int): ID do usuario do que se queren borrar a relación de poles.
        db (Session): Sesión da base de datos.

    Raises:
        Exception: Recolle calquera tipo de excepción e devolve a base de datos
                ao seu estado anterior, imprimindo un erro.
    """
    try:
        user_pollens = (
            db.query(UserPollens).filter(UserPollens.user_id == user_id).all()
        )
        if user_pollens:
            for user_pollen in user_pollens:
                db.delete(user_pollen)
            db.commit()
        else:
            print(f"Non hai rexistros para eliminar do user {user_id}.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao tentar borrar os rexistros: {e}")


def delete_user_logs(user_id, db: Session):
    """
    Función para eliminar filas de user_logs dun usuario, dado o seu ID.

    Args:
        user_id (int): ID do usuario do que se queren borrar os rexistros.
        db (Session): Sesión da base de datos.

    Returns:
        Nada

    Raises:
        Exception: Se ocurre algún erro no proceso. Devolve a base de datos ao estado
                anterior e imprime un erro.
    """

    try:
        user_logs = db.query(UserLog).filter(UserLog.user_id == user_id).all()
        if user_logs:
            for user_log in user_logs:
                db.delete(user_log)
            db.commit()
        else:
            print(f"Non hai rexistros para eliminar do user {user_id}.")
    except Exception as e:
        # Reverte os cambios
        db.rollback()
        print(f"Erro ao tentar borrar os rexistros: {e}")


# ==============================================================================
# OUTRAS
# ==============================================================================


def get_user_from_db(username: str, db: Session = Depends(get_db)):
    """
    Función para obter un usuario da base de datos, dado o seu nome de usuario.

    Args:
        username: Nome do usuario.
        db (Session): Sesión da base de datos.

    Returns:
        User: instancia de usuario
    """

    user = db.query(User).filter(User.username == username).first()

    return user


# Crea un contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
