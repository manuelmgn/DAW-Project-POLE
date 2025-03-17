"""Funcións auxiliares para a definición das rutas"""

from functools import wraps
from flask import jsonify, redirect, session, url_for
from config.config import Config
import requests

config = Config()


def check_user(id):
    """
    Comproba se un usuario existe na base de datos

    Args:
        id (int): ID do usuario.
    
    Returns:
        bool: True se o usuario existe, False se non.
    """
    response = requests.get(
        f"{config.FASTAPI_URL}/user/{id}",
        headers={
            "Content-Type": "application/json",
            "x-api-key": config.API_KEY,
        },
    )

    if response.status_code == 200:
        return True
    else:
        return False


def format_timestamp(timestamp):
    """
    Formatea un timestamp nunha cadea de texto

    Args:
        timestamp (datetime): Timestamp para formatear.
    
    Returns:
        str: Timestamp formateado.
    """

    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def simplify_location(location):
    """
    Recolle unha localización, dividea en partes
    e devolve estas partes nun string.

    Args:
        location (dict): Localización a simplificar.
    
    Returns:
        str: Localización simplific
    """
    loc_split = location["name"].split(",")

    if len(loc_split) > 3:
        loc_unido = ",".join(loc_split[:3])
    else:
        loc_unido = location["name"]

    return loc_unido


def get_pollen_types():
    """
    Obten os tipos de pole almacenados na base de datos.

    Returns:
        list: Lista de tipos de pole.
    """

    response = requests.get(
        f"{config.FASTAPI_URL}/pollen-types/",
        headers={"x-api-key": config.API_KEY},
    )

    if response.status_code == 200:
        return response.json()
    
    return []


def login_required(f):
    """
    Decorador para exixir o inicio de sesión para acceder á web.

    Args:
        f (function): Función a decorar.
    
    Returns:
        function: Función decorada.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "id_user" not in session:  # Verifica si el usuario está logueado
            return redirect(
                url_for("auth_bp.login")
            )  # Redirige al login si no está autenticado
        return f(*args, **kwargs)

    return decorated_function


def call_api_key(subroute, id):
    """
    Chama a unha subruta da API de FastAPI.

    Args:
        subroute (str): Subruta da API.
        id (int): ID do elemento a buscar.
    
    Returns:
        requests.models.Response: Resposta da API.
    """
    url = f"{config.FASTAPI_URL}/{subroute}/{id}"
    response = requests.get(
        url,
        headers={"x-api-key": config.API_KEY},
    )
    return response


def get_near_userlogs(lat: float, lon: float):
    """
    ESTA FUNCIÓN FOI DESEÑADA POR UNHA IA E MODIFICADA POR MIN
    Devolve os rexistros de usuario máis próximos a unha localización.

    Args:
        lat (float): Latitude.
        lon (float): Lonxitude.
    
    Returns:
        dict: Información sobre os rexistros de usuario.

    Raises:
        requests.RequestException: Se hai un erro ao chamar á API.
    """

    if not lat or not lon:
        return (
            jsonify(
                {
                    "error": "Coordenadas non proporcionadas",
                    "nearby_ratings": [],
                    "average_rating": None,
                    "count": 0,
                }
            ),
            400,
        )

    try:
        # Llamar a la API de FastAPI
        url = f"{config.FASTAPI_URL}/userlogs/near/"
        params = {
            "lat": lat,
            "lon": lon,
            "max_distance": 20,  # Puedes hacer esto configurable
        }

        response = requests.get(
            url, params=params, headers={"x-api-key": config.API_KEY}
        )

        # Devolver directamente el JSON si el código de estado es 200
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "nearby_ratings": [],
                "average_rating": None,
                "count": 0,
                "error": response.text,
            }

    except requests.RequestException as e:
        return {
            "nearby_ratings": [],
            "average_rating": None,
            "count": 0,
            "error": str(e),
        }


def get_userlog_by_loc(location):
    """
    Devolve os rexistros de usuario por localización.

    Args:
        location (dict): Localización.
    
    Returns:
        dict: Información sobre os rexistros de usuario.
    
    Raises:
        requests.RequestException: Se hai un erro ao chamar á API.
    """

    coordinates = location["coordinates"]

    if not coordinates or len(coordinates) < 2:
        info = {"nearby_ratings": [], "average_rating": None, "count": 0}
    else:
        lat = coordinates[0]
        lon = coordinates[1]
        info = get_near_userlogs(lat, lon)

    # Acceder a datos específicos
    nearby_ratings = info.get("nearby_ratings", [])
    average_rating = info.get("average_rating", None)
    count = info.get("count", 0)

    # Planifico a resposta
    if average_rating:
        if average_rating >= 0 and average_rating < 2:
            resposta = {
                "severity": average_rating,
                "message": "👌 Os usuarios non están a experimentar ningún tipo de síntoma de alerxia ao pole nesta zona.",
                "color": "green",
            }
        if average_rating >= 2 and average_rating < 3:
            resposta = {
                "severity": average_rating,
                "message": "👍 Parece que algunhas persoas da nosa comunidade neste lugar están a sofrer síntomas puntuais.",
                "color": "var(--cor3)",
            }
        if average_rating >= 3 and average_rating < 4:
            resposta = {
                "severity": average_rating,
                "message": "⚠️ Ollo! Algunhas persoas están a rexistrar síntomas moderados de alerxia nesta zona.",
                "color": "var(--cor4)",
            }
        if average_rating >= 4 and average_rating <= 5:
            resposta = {
                "severity": average_rating,
                "message": "🚨 Moito coidado! Os usuarios desta localización están a sofrer síntomas de alerxias moi fortes.",
                "color": "var(--cor5)",
            }
    else:
        resposta = {
            "severity": "Sen datos",
            "message": "A nosa comunidade de usuarios non fixo ningún rexistros na túa zona nos últimos días 😓. Fai ti o primeiro e comparte a app!",
            "color": "gray",
        }

    return resposta


def get_pollen_names_by_user(user_id):
    """
    Obten os nomes dos tipos de pole que un usuario ten alerxia.

    Args:
        user_id (int): ID do usuario.
    
    Returns:
        list: Lista de tipos de pole
    """
    
    response_user_pollens = requests.get(
        f"{config.FASTAPI_URL}/pollen-types/{user_id}",
        headers={"x-api-key": config.API_KEY},
    )

    response_pollens = requests.get(
        f"{config.FASTAPI_URL}/pollen-types/",
        headers={"x-api-key": config.API_KEY},
    )

    if (
        response_pollens.status_code == 200
        and response_user_pollens.status_code == 200
    ):
        response_user_pollens = response_user_pollens.json()
        response_pollens = response_pollens.json()

        resposta = []
        for user_pollen in response_user_pollens:
            for pollen in response_pollens:
                if pollen["id_pollen"] == user_pollen["pollen_id"]:
                    resposta.append(
                        [pollen["pollen_name"], pollen["pollen_gal"]]
                    )

        return resposta
    else:
        return redirect(url_for("auth_bp.login"))
