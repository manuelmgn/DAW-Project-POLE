"""Router cos endpoints de usuarios"""

from fastapi import APIRouter, Depends, HTTPException, Header
import requests
from sqlalchemy.orm import Session
from typing import List

from external_apis.utils import get_pollen_level_description
from database.database import get_db
from security import validate_api_key

router = APIRouter()

# ==============================================================================
# TEMPO METEOROLÓXICO
# ==============================================================================


# ------------------------------------------------------------------------------
# Actualmente
# ------------------------------------------------------------------------------


@router.post("/current_weather", tags=["External APIs"])
def get_current_weather(
    coordinates: List[str],
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Ruta para obter a información actual do tempo a través da API Open-Meteo.

    Args:
        coordinates (List[str]): Lista de coordenadas (latitude e lonxitude).
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Returns:
        dict: Dicionario coa información actual do tempo.

    Raises:
        HTTPException: Se a chave da API non é válida.
        HTTPException: Se as coordenadas proporcionadas son inválidas.
        HTTPException: Se hai un erro ao obter os datos do tempo.
        HTTPException: Se hai un erro ao conectarse á API.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    if len(coordinates) < 2:
        raise HTTPException(status_code=400, detail="Invalid coordinates")

    latitude, lonxitude = coordinates[0], coordinates[1]

    try:
        # Obtemos os weather codes
        weather_codes_url = "https://gist.githubusercontent.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c/raw/76b0cb0ef0bfd8a2ec988aa54e30ecd1b483495d/descriptions.json"

        response = requests.get(weather_codes_url)
        weather_codes = response.json() if response else {}

        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={lonxitude}&current_weather=true"

        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            datos = respuesta.json()

            # Extraemos a información que vamos usar
            current_weather = {
                "temperature": datos["current_weather"]["temperature"],
                "windspeed": datos["current_weather"]["windspeed"],
                "winddirection": datos["current_weather"]["winddirection"],
                "weather_code": datos["current_weather"]["weathercode"],
                "description": "",
                "image": "",
            }

            weather_code_str = str(current_weather["weather_code"])

            if weather_code_str in weather_codes:
                current_weather.update(
                    {
                        "description": weather_codes[weather_code_str][
                            "night"
                        ]["description"],
                        "image": weather_codes[weather_code_str]["night"][
                            "image"
                        ],
                    }
                )

            return current_weather
        else:
            raise HTTPException(
                status_code=respuesta.status_code,
                detail="Error fetching weather data",
            )

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to API: {str(e)}"
        )


# ------------------------------------------------------------------------------
# Pronóstico
# ------------------------------------------------------------------------------


@router.post("/forecast_weather", tags=["External APIs"])
def get_weather_forecast(
    coordinates: List[str],
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Obtén a previsión meteorolóxica para as coordenadas dadas usando a API de Open-Meteo.

    Args:
        coordinates (List[str]): Lista de coordenadas con latitude e lonxitude.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Raises:
        HTTPException: Se a chave API é inválida, as coordenadas son inválidas, ou hai un
            erro ao obter os datos meteorolóxicos.

    Returns:
        dict: Dicionario coa previsión meteorolóxica.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    if len(coordinates) < 2:
        raise HTTPException(status_code=400, detail="Invalid coordinates")

    latitude, lonxitude = coordinates[0], coordinates[1]

    try:
        weather_codes_url = "https://gist.githubusercontent.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c/raw/76b0cb0ef0bfd8a2ec988aa54e30ecd1b483495d/descriptions.json"

        response = requests.get(weather_codes_url)
        weather_codes_sheet = response.json() if response else {}

        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={lonxitude}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,showers_sum,precipitation_hours,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant&timezone=Europe%2FBerlin"

        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            datos = respuesta.json()

            forecast = {
                "weather_code": datos["daily"]["weather_code"],
                "temperature_2m_max": datos["daily"]["temperature_2m_max"],
                "temperature_2m_min": datos["daily"]["temperature_2m_min"],
                "precipitation_sum": datos["daily"]["precipitation_sum"],
                "precipitation_hours": datos["daily"]["precipitation_hours"],
                "rain_sum": datos["daily"]["rain_sum"],
                "showers_sum": datos["daily"]["showers_sum"],
                "wind_speed_10m_max": datos["daily"]["wind_speed_10m_max"],
                "wind_gusts_10m_max": datos["daily"]["wind_gusts_10m_max"],
                "wind_direction_10m_dominant": datos["daily"][
                    "wind_direction_10m_dominant"
                ],
                "description": "",
                "image": "",
            }

            descriptions = []
            images = []
            weather_codes = forecast["weather_code"]

            for code in weather_codes:
                code = str(code)
                if code in weather_codes_sheet:
                    descriptions.append(
                        weather_codes_sheet[code]["night"]["description"]
                    )
                    images.append(weather_codes_sheet[code]["night"]["image"])

            forecast.update({"description": descriptions, "image": images})

            return forecast
        else:
            raise HTTPException(
                status_code=respuesta.status_code,
                detail="Error fetching weather data",
            )

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Error connecting to API: {str(e)}"
        )


# ==============================================================================
# POLE NO AR
# ==============================================================================


# ------------------------------------------------------------------------------
# Actualmente
# ------------------------------------------------------------------------------
@router.post("/current_pollen", tags=["External APIs"])
def get_pollen_by_loc(
    coordinates: List[str],
    db: Session = Depends(get_db),
    x_api_key: str = Header(...),
):
    """
    Obtén información actual do pole da API Open-Meteo baseada nas coordenadas proporcionadas.

    Args:
        ccoordinates (List[str]): Lista de coordenadas con latitude e lonxitude.
        db (Session): Sesión da base de datos.
        x_api_key (str): Chave API.

    Raises:
        HTTPException: Se a lista de coordenadas ten menos de 2 elementos.
        requests.RequestException: Se hai un erro ao facer a solicitude á API Open-Meteo.

    Returns:
        dict: Dicionario con descricións dos niveis de pole.
    """

    # Verificamos a API Key
    validate_api_key(x_api_key)

    if len(coordinates) < 2:
        raise HTTPException(status_code=400, detail="Invalid coordinates")

    latitude, lonxitude = coordinates[0], coordinates[1]

    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={lonxitude}&current=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        # Datos actuais
        current_pollen = data.get("current", {})

        # Recollo a información para cada tipo
        # Non uso os meus poles porque isto depende da API
        pollens = {
            "alder": current_pollen.get("alder_pollen", [None]),
            "birch": current_pollen.get("birch_pollen", [None]),
            "grass": current_pollen.get("grass_pollen", [None]),
            "mugwort": current_pollen.get("mugwort_pollen", [None]),
            "olive": current_pollen.get("olive_pollen", [None]),
            "ragweed": current_pollen.get("ragweed_pollen", [None]),
        }


        # Introduzo datos textuais
        pollens_desc = {
            tipo: get_pollen_level_description(valor)
            for tipo, valor in pollens.items()
        }

        return pollens_desc

    except requests.RequestException as e:
        print(f"Erro ao obter datos do pole: {e}")
        return None
