"""Router cos endpoints de usuarios"""

from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from database.database import get_db
from database.relations import UserPollens
from database.utils import delete_user_logs, delete_user_pollens
from users.functions import verify_existing_user
from users.schemas import *
from users.models import User
from security import get_password_hash, validate_api_key
from pollens.models import Pollen

router = APIRouter()

# ==============================================================================
# USERS CRUD: GET (READ)
# ==============================================================================

# ------------------------------------------------------------------------------
# GET USERS
# ------------------------------------------------------------------------------


@router.get("/", response_model=List[UserResponse], tags=["Users"])
def get_users(
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
    includeAdmins=False,
) -> List[UserResponse]:
    """
    Función para obter todos os usuarios

    Args:
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.
        includeAdmins (bool): Se se queren incluír os administradores.

    Returns:
        List[UserResponse]: Lista de usuarios obtidos
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    # Recolle os datos dos usuarios (con excepción das relacións)
    if includeAdmins:
        users = db.query(User).all()
    else:
        users = db.query(User).filter(User.role != "admin").all()

    # Devolve os datos
    return [UserResponse.model_validate(user) for user in users]


# ------------------------------------------------------------------------------
# GET USERS BY ID
# ------------------------------------------------------------------------------


@router.get("/{id}", response_model=UserResponse, tags=["Users"])
def get_user_id(
    id: int, db: Session = Depends(get_db), x_api_key: str = Header(...)
) -> UserResponse:
    """
    Función para obter un usuario polo seu ID.

    Args:
        id (int): id do usuario desexado.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        UserResponse: Usuario obtido.

    Raises:
        HTTPException: Se o usuario non existe.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    user = db.query(User).filter(User.id_user == id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Usuario non encontrado")

    return UserResponse.model_validate(user)


# ==============================================================================
# USERS CRUD: POST (CREATE)
# ==============================================================================

# ------------------------------------------------------------------------------
# POST NEW USER
# ------------------------------------------------------------------------------


@router.post("/", response_model=UserResponse, tags=["Users"])
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para crear un usuario básico na base de datos.

    Args:
        user(UserCreate): Datos do usuario
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        UserResponse: Usuario creado.

    Raises:
        HTTPException: Se hai algún erro de validación ou de integridade.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        # Verificación dos id introducidos
        if hasattr(user, "pollen_allergies"):
            existing_pollens = (
                db.query(Pollen)
                .filter(Pollen.id_pollen.in_(user.pollen_allergies))
                .all()
            )

            if len(existing_pollens) != len(user.pollen_allergies):
                raise HTTPException(
                    status_code=400,
                    detail="Algún dos ID de pole introducidos non existen na base de datos",
                )

        # Creación do contrasinal hasheado
        hashed_password = get_password_hash(user.password)

        # Converte o obxecto Location a dicionario
        location_dict = user.location.model_dump()

        # Creamos unha configuración por defecto
        config = Config(fav_locations=[user.location])
        config_dict = config.model_dump()

        # Creación do usuario (sen chegar a escribilo)
        db_user = User(
            name=user.name,
            lastname=user.lastname,
            email=user.email,
            username=user.username,
            password=hashed_password,
            birthdate=user.birthdate,
            location=location_dict,
            role="basic",
            enabled=True,
            config=config_dict,
        )

        # Engade o usuario á DB (sen confirmar aínda)
        db.add(db_user)

        # Obter o ID do usuario, evitando ter que facer commit previamente
        db.flush()

        if not isinstance(db_user.id_user, int):
            raise ValueError("O id_user non é un número enteiro")

        # Escribe as relacións usuario-alerxias na táboa correspondente
        if hasattr(user, "pollen_allergies"):
            for pollen_id in user.pollen_allergies:
                new_user_pollens = UserPollens(
                    user_id=db_user.id_user, pollen_id=pollen_id
                )
                db.add(new_user_pollens)

        # Fai commit dos cambios
        db.commit()

        # Refresca
        db.refresh(db_user)

        # Retorna o usuario co modelo de resposta
        return UserResponse.model_validate(db_user)

    # Excepción en caso de erro de validación
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Excepción en caso de erro de integridade
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="O username ou o email xa existen na base de datos",
        )

    # Recolle outras excepcións
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}"
        )


# ==============================================================================
# USERS CRUD: PUT (UPDATE)
# ==============================================================================

# ------------------------------------------------------------------------------
# UPDATE COMPLETO DE USUARIO POR ADMIN
# ------------------------------------------------------------------------------


@router.put("/{id}/admin", response_model=UserResponse, tags=["Users"])
def update_user_complete(
    id: int,
    user: UserCompleteEdition,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para actualizar por completo un usuario existente

    Args:
        id (int): Id do usuario que queremos actualizar
        user (UserCompleteEdition): Datos novos do usuario
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        UserResponse: Usuario actualizado

    Raises:
        HTTPException: Se o usuario non existe ou se ten conflictos
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        verify_existing_user(id, db)

        email_exists = (
            db.query(User)
            .filter(User.email == user.email, User.id_user != id)
            .first()
        )
        username_exists = (
            db.query(User)
            .filter(
                User.username == user.username,
                User.id_user != id,
            )
            .first()
        )

        if email_exists:
            raise HTTPException(
                status_code=400, detail="O email xa está a ser usado"
            )
        if username_exists:
            raise HTTPException(
                status_code=400, detail="O username xa está a ser usado"
            )

        hashed_password = get_password_hash(user.password)

        db.query(User).filter(User.id_user == id).update(
            {
                User.name: user.name,
                User.lastname: user.lastname,
                User.email: user.email,
                User.username: user.username,
                User.password: hashed_password,
                User.birthdate: user.birthdate,
                User.location: user.location,
                User.role: user.role,
                User.enabled: user.enabled,
            }
        )

        db.commit()

        updated_user = db.query(User).filter(User.id_user == id).first()
        return UserResponse.model_validate(updated_user)

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


# ------------------------------------------------------------------------------
# UPDATE COMPLETO BÁSICO
# ------------------------------------------------------------------------------


@router.put("/{id}", response_model=UserResponse, tags=["Users"])
def update_user_basic(
    id: int,
    user: UserBase,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para actualizar un usuario existente.

    Args:
        id (int): ID do usuario que queremos actualizar.
        user (UserBasicEdition): Datos novos do usuario.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        UserResponse: Usuario actualizado

    Raises:
        HTTPException: Se o usuario non existe ou se ten conflictos.

    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        verify_existing_user(id, db)

        email_exists = (
            db.query(User)
            .filter(User.email == user.email, User.id_user != id)
            .first()
        )

        if email_exists:
            raise HTTPException(
                status_code=400, detail="O email xa está a ser usado"
            )

        location_dict = user.location.model_dump()

        db.query(User).filter(User.id_user == id).update(
            {
                User.name: user.name,
                User.lastname: user.lastname,
                User.email: user.email,
                User.birthdate: user.birthdate,
                User.location: location_dict,
            }
        )

        db.commit()

        updated_user = db.query(User).filter(User.id_user == id).first()
        return UserResponse.model_validate(updated_user)

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


# ------------------------------------------------------------------------------
# UPDATE NOME
# ------------------------------------------------------------------------------


@router.put("/{id}/name", response_model=UserResponse, tags=["Users"])
def update_user_names(
    id: int,
    user: UserNameEdition,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para actualizar o nome dun usuario existente.

    Args:
        id (int): Id do usuario que queremos actualizar.
        user (UserNameEdition): Datos novos do usuario.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        UserResponse: Usuario actualizado.

    Raises:
        HTTPException: Se o usuario non existe ou se ten conflictos.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        verify_existing_user(id, db)

        db.query(User).filter(User.id_user == id).update(
            {User.name: user.name, User.lastname: user.lastname}
        )

        db.commit()

        updated_user = db.query(User).filter(User.id_user == id).first()
        return UserResponse.model_validate(updated_user)

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


# ------------------------------------------------------------------------------
# UPDATE PASS
# ------------------------------------------------------------------------------


@router.put("/{id}/pass", response_model=UserResponse, tags=["Users"])
def update_user_pass(
    id: int,
    user: UserPassEdition,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para actualizar o contrasinal dun usuario existente

    Args:
        id (int): Id do usuario que queremos actualizar
        user (UserPassEdition): Datos novos do usuario
        db (Session): Sesión da base de datos.

    Returns:
        UserResponse: Usuario actualizado

    Raises:
        HTTPException: Se o usuario non existe ou se ten conflictos
    """
    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        verify_existing_user(id, db)

        hashed_password = get_password_hash(user.password)

        db.query(User).filter(User.id_user == id).update(
            {User.password: hashed_password}
        )

        db.commit()

        return "Contrasinal modificado satisfactoriamente"

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


# ------------------------------------------------------------------------------
# UPDATE LOCALIZACION
# ------------------------------------------------------------------------------


@router.put("/{id}/location", response_model=UserResponse, tags=["Users"])
def update_user_location(
    id: int,
    user: UserLocEdition,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para actualizar a localización dun usuario existente.

    Args:
        id (int): Id do usuario que queremos actualizar
        user (UserLocEdition): Datos novos do usuario
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        UserResponse: Usuario actualizado.

    Raises:
        HTTPException: Se o usuario non existe ou se ten conflictos.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        verify_existing_user(id, db)

        db.query(User).filter(User.id_user == id).update(
            {
                User.location: user.location,
            }
        )

        db.commit()

        updated_user = db.query(User).filter(User.id_user == id).first()
        return UserResponse.model_validate(updated_user)

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


# ------------------------------------------------------------------------------
# UPDATE ALERXIAS
# ------------------------------------------------------------------------------


@router.put("/{id}/allergies", tags=["Users"])
def update_user_allergies(
    id: int,
    user: UserallergiesEdition,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para actualizar as alerxias dun usuario existente

    Args:
        id (int): Id do usuario que queremos actualizar.
        user (UserallergiesEdition): Datos novos do usuario.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        UserResponse: Usuario actualizado

    Raises:
        HTTPException: Se o usuario non existe ou se ten conflictos
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        # Comproba se o usuario existe
        verify_existing_user(id, db)

        # Verificación dos id introducidos
        if hasattr(user, "pollen_allergies"):
            existing_pollens = (
                db.query(Pollen)
                .filter(Pollen.id_pollen.in_(user.pollen_allergies))
                .all()
            )

            if len(existing_pollens) != len(user.pollen_allergies):
                raise HTTPException(
                    status_code=400,
                    detail="Algúns dos ID de pole introducidos non existe na base de datos",
                )

        # Borra as filas correspondentes
        delete_user_pollens(id, db)

        # Escribe as relacións usuario-alerxias na táboa correspondente
        if hasattr(user, "pollen_allergies"):
            for pollen_id in user.pollen_allergies:
                new_user_pollen = UserPollens(user_id=id, pollen_id=pollen_id)
                db.add(new_user_pollen)

        # Fai commit dos cambios
        db.commit()

        return "Alerxias modificadas correctamente"

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


# ------------------------------------------------------------------------------
# DESACTIVAR USER
# ------------------------------------------------------------------------------


@router.put("/deactivate/{id}", tags=["Users"])
def deactivate_user(
    id: int,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para desactivar un usuario existente.

    Args:
        id (int): Id do usuario que queremos actualizar
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        dict: Mensaxe de confirmación.

    Raises:
        HTTPException: Se o usuario non existe ou se ten conflictos
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        verify_existing_user(id, db)

        user = db.query(User).filter(User.id_user == id).first()
        if user is None:
            raise HTTPException(
                status_code=404, detail="Usuario non encontrado"
            )

        # Actualizamos o estado do usuario
        user.enabled = not user.enabled

        db.commit()

        return {"message": f"O usuario co ID {id} foi (des)activado"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# USERS CRUD: DELETE
# ==============================================================================

# ------------------------------------------------------------------------------
# DELETE BY ID
# ------------------------------------------------------------------------------


@router.delete("/{id}", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_user(
    id: int, db: Session = Depends(get_db), x_api_key: str = Header(...)
):
    """
    Función para eliminar un usuario existente.

    Args:
        id (int): ID do usuario que queremos eliminar.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        dict: Mensaxe de confirmación.

    Raises:
        HTTPException: Se o usuario non existe ou se ten conflictos.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        user = (
            db.query(User)
            .filter(User.id_user == id, User.role != "admin")
            .first()
        )
        if user is None:
            raise HTTPException(
                status_code=404, detail="Usuario non encontrado"
            )

        # Borramos a súa relacións cos tipos de pole na táboa intermedia
        delete_user_pollens(id, db)

        # Borramos os seus rexistros de alerxia
        delete_user_logs(id, db)

        # Borramos o usuario
        db.delete(user)

        # Confirmamos os cambios
        db.commit()

        return {"message": f"O usuario co ID {id} foi eliminado"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# ACTUALIZAR CONFIG
# ==============================================================================

# ------------------------------------------------------------------------------
# Config locations
# ------------------------------------------------------------------------------


@router.post(
    "/{id}/config/locations", status_code=status.HTTP_200_OK, tags=["Users"]
)
def update_config_locations(
    id: int,
    locations: List[Location],
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Actualiza as localizacións secundarias do usuario

    Args:
        id (int): ID do usuario.
        locations (List[Location]): Lista de localizacións.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        dict: Mensaxe de confirmación.

    Raises:
        HTTPException: Se o usuario non existe ou se ten conflictos.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    if not 1 <= len(locations) <= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Débense proporcionar 1-3 localizacións",
        )

    # Procurar o usuario
    user = db.query(User).filter(User.id_user == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario non encontrado",
        )
    new_locations = []

    for location in locations:
        location_dict = location.model_dump()
        new_locations.append(location_dict)

    config = Config(fav_locations=new_locations)

    db.query(User).filter(User.id_user == id).update(
        {
            User.config: config.model_dump(),
        }
    )

    db.commit()
    db.refresh(user)

    return {"message": "Localizacións actualizadas satisfactoriamente"}
