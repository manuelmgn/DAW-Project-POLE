"""Router para os tipos de pole"""

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from pollens.utils import load_pollen_types
from database.relations import UserPollens
from users.functions import verify_existing_user
from security import validate_api_key
from pollens.schemas import PollenResponse
from auth import router
from database.database import get_db
from .models import Pollen

router = APIRouter()

# ==============================================================================
# CRUD
# ==============================================================================


# ------------------------------------------------------------------------------
# GET
# ------------------------------------------------------------------------------


@router.get("/", response_model=List[PollenResponse], tags=["Pollens"])
def get_pollen_types(
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Devolve os tipos de pole.

    Args:
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        List[PollenResponse]: Lista de tipos de pole.

    Raises:
        HTTPException: Se a chave da API é inválida.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    load_pollen_types(db)

    # Retorna todos os tipos de pole
    return db.query(Pollen).all()


@router.get("/{id}", tags=["Pollens"])
def get_pollen_types_by_user(
    id: int,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Devolve os tipos de pole aos que é alérxico un usuario, dado o seu ID

    Args:
        id (int): Id do usuario.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        List[UserPollens]: Lista de tipos de pole aos que é alérxico o usuario.

    Raises:
        HTTPException: Se a chave API é inválida.
        HTTPException: Se o usuario non existe.
        HTTPException: Se hai un erro de integridade na base de datos.
        HTTPException: Se hai algún outro erro interno.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        verify_existing_user(id, db)

        user_pollens = db.query(UserPollens).filter_by(user_id=id).all()

        return user_pollens

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Erro de integridade na base de datos"
        )

    except HTTPException as http_ex:
        db.rollback()
        raise http_ex

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}"
        )
