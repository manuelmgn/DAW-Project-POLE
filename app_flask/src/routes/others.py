"""Miscelánea de rutas que non encaixan en ningún outro blueprint"""

from flask import (
    Blueprint,
    redirect,
    render_template,
    session,
    url_for,
)
import requests
from utils.utils import (
    get_pollen_names_by_user,
    get_userlog_by_loc,
    login_required,
    simplify_location,
)
from config.config import Config

others_bp = Blueprint("others_bp", __name__)
config = Config()


@others_bp.route("/maps", methods=["GET"])
@login_required
def get_map():
    """
    Mostra o mapa principal de rexistros
    """

    days = 2

    url = f"{config.FASTAPI_URL}/userlogs/recent/{days}"

    response = requests.get(
        url,
        headers={"x-api-key": config.API_KEY},
    )

    if response.status_code == 200:
        recent_userlogs = response.json()
    else:
        raise Exception(f"Non se encontraron userlogs. {response.text}")

    return render_template("userlogs/map.html", userlogs=recent_userlogs)


@others_bp.route("/forecast", methods=["GET"])
@login_required
def get_forecast():
    """
    Mostra a previsión do tempo para a localización principal e as favoritas
    """

    # Primeiro comprobo se é admin, para introducir un link
    # á sección de admin
    if session.get("admin"):
        is_admin = True
    else:
        is_admin = False

    id_user = session.get("id_user")
    name = session.get("name")

    if id_user:

        id = int(id_user)

        # Procuro a localización principal na info de sesión
        loc_first = session.get("location", {})
        loc_second = session.get("config", {}).get("fav_locations", "")[0]

        if loc_first == loc_second:
            loc_second = None

        locations = [loc_first, loc_second]

        locations_info = []
        for location in locations:
            if location:

                coordinates = location.get("coordinates", [])

                # Recollo o WEATHER
                url = f"{config.FASTAPI_URL}/external-apis/forecast_weather"

                response = requests.post(
                    url,
                    json=coordinates,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": config.API_KEY,
                    },
                )

                if response.status_code == 200:
                    weather_data = response.json()

                    if weather_data:
                        locations_info.append(
                            [
                                simplify_location(location),
                                weather_data,
                            ]
                        )
                    else:
                        raise Exception("Problema devolvendo a resposta")

        get_pollen_names_by_user(id_user)

        return render_template(
            "/various/forecast.html",
            locations=locations_info,
            is_admin=is_admin,
            name=name,
        )
    else:
        return redirect(url_for("auth_bp.login"))
