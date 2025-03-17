"""Funcións de seguridade"""

from fastapi import HTTPException, Header
from passlib.context import CryptContext

from config import API_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """
    Función para obter o hash dun contrasinal

    Args:
        password (str): Contrasinal a hashear.

    Returns:
        str: Hash do contrasinal.
    """
    return pwd_context.hash(password)


def validate_api_key(x_api_key: str = Header(...)):
    """
    Función para verificar se unha chamada se realiza usando a chave correcta.

    Args:
        x_api_key (str): Chave API.

    Raises:
        HTTPException: Se a chave non é a correcta.
    """

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Acceso denegado")
