"""Modelos para a autentificación de usuarios."""

from pydantic import BaseModel


class LoginData(BaseModel):
    """
    Modelo LoginData para a autentificación de usuarios.

    Atributos:
        username (str): Nome de usuario.
        password (str): Contrasinal do usuario.
    """

    username: str
    password: str
