"""Router cos endpoints da autentificación de usuarios"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import bcrypt

from security import validate_api_key
from auth import models
from database.database import get_db
from database.utils import get_user_from_db

router = APIRouter()


@router.post("/login", tags=["Auth"])
def login(
    data: models.LoginData,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Manexa o login.

    Args:
        data (models.LoginData): Datos de login
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Raises:
        HTTPException: Se a chave da API é inválida.
        HTTPException: Se o nome de usuario ou o contrasinal son incorrectos.

    Returns:
        dict: Dicionario que contén información do usuario, con excepción do contrasinal.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    user = get_user_from_db(data.username, db)
    if not user or not bcrypt.checkpw(
        data.password.encode("utf-8"), user.password.encode("utf-8")
    ):
        raise HTTPException(
            status_code=400, detail="Nome de usuario ou contrasinal inválidos"
        )

    # Devolver datos do usuario sen o contrasinal
    return {
        "id_user": user.id_user,
        "username": user.username,
        "role": user.role,
        "location": user.location,
        "config": user.config,
        "name": user.name,
    }
