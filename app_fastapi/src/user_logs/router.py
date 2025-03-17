"""Router dos logs cos seus endpoints"""

from datetime import timedelta
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from user_logs.utils import haversine_distance
from security import validate_api_key
from users.functions import get_user_location
from user_logs.models import UserLog
from user_logs.schemas import *
from database.database import get_db
from users.models import User

router = APIRouter()

# ==============================================================================
# GET
# ==============================================================================


@router.get("/recent/{days_input}", tags=["User logs"])
def get_recent_logs(
    days_input: int,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para obter os rexistros dos usuarios dos últimos días

    Args:
        days_input (int): Número de días a considerar.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        List[UserLog]: Lista de rexistros recentes do usuario.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    # Calculamos a data limite
    limit_date = datetime.now() - timedelta(days=days_input)

    # Almacenamos os logs recentes
    logs_recents = (
        db.query(UserLog).filter(UserLog.timestamp >= limit_date).all()
    )

    # Devolvémos os logs recentes
    return logs_recents


@router.get("/{user_id}", tags=["User logs"])
def get_logs_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para obter todos os rexistros dun usuario

    Args:
        user_id (int): ID do usuario.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        List[UserLog]: Lista de rexistros do usuario.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    logs = (
        db.query(UserLog)
        .filter(UserLog.user_id == user_id)
        .order_by(UserLog.timestamp.desc())
        .all()
    )
    return logs


# ==============================================================================
# POST
# ==============================================================================


@router.post(
    "/new-userlog/", response_model=UserLogResponse, tags=["User logs"]
)
def create_userlog(
    user_log: UserLogCreate,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Función para crear un novo rexistro de usuario

    Args:
        user_log (UserLogCreate): Datos do rexistro.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        UserLogResponse: Datos do rexistro creado.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    try:
        # Verificamos o usuario
        user = db.query(User).filter(User.id_user == user_log.user_id).first()

        # Se non existe, enviamos un erro
        if not user:
            raise HTTPException(
                status_code=404, detail="Usuario non encontrado"
            )

        # Asignamos a localización e se non existe collemos a marcada por defecto
        if user_log.location:
            location = user_log.location
        else:
            location = get_user_location(user_log.user_id, db)

        # Novo userlog
        db_userlog = UserLog(
            severity=user_log.severity,
            timestamp=user_log.timestamp,
            location=location.dict(),
            user_id=user_log.user_id,
        )

        db.add(db_userlog)
        db.commit()
        db.refresh(db_userlog)
        return UserLogResponse.model_validate(db_userlog)

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
# INFORMACIÓN DE LOGS CERCANOS
# ==============================================================================


# Ruta de FastAPI para obtener logs cercanos
@router.get("/near/", response_model=Dict, tags=["User logs"])
async def get_nearby_userlogs(
    lat: float,
    lon: float,
    max_distance: float = 50.0,
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    ESTA FUNCIÓN FOI DESEÑADA POR UNHA IA E MODIFICADA POR MIN
    Función para obter os logs cercanos a unha localización dada

    Args:
        lat (float): Latitude da localización.
        lon (float): Lonxitude da localización.
        max_distance (float): Distancia máxima para considerar un log.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        Dict: Dicionario coa información dos logs cercanos.

    Raises:
        Exception: Se non hai rexistros recentes.
    """

    validate_api_key(x_api_key)

    # Obtener logs de los últimos 2 días
    two_days_ago = datetime.now() - timedelta(days=2)

    # Consulta para obtener logs recientes con sus coordenadas
    recent_logs = (
        db.query(UserLog).filter(UserLog.timestamp >= two_days_ago).all()
    )

    if not recent_logs:
        raise Exception("Non hai rexistros recents")

    # Filtrar y calcular logs cercanos
    nearby_ratings = []
    for log in recent_logs:
        # Extraer coordenadas del JSON de location
        loc_coords = log.location.get("coordinates", [])
        # Verificar que tengamos coordenadas válidas
        if len(loc_coords) >= 2:
            try:
                log_lat, log_lon = float(loc_coords[0]), float(loc_coords[1])

                # Calcular distancia
                distance = haversine_distance(lat, lon, log_lat, log_lon)

                # Si está dentro del radio, agregar
                if distance <= max_distance:
                    nearby_ratings.append(log.severity)
            except (ValueError, TypeError):
                # Ignorar logs con coordenadas inválidas
                continue

    # Calcular promedio
    if nearby_ratings:
        average_rating = sum(nearby_ratings) / len(nearby_ratings)
        return {
            "nearby_ratings": nearby_ratings,
            "average_rating": round(average_rating, 2),
            "count": len(nearby_ratings),
        }

    return {"nearby_ratings": [], "average_rating": None, "count": 0}
