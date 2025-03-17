"""Rutas principais da aplicación"""

from flask import Blueprint, jsonify, render_template, request, session

from utils.utils import *
from utils.utils import login_required
from templates import *

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def index():
    """
    Función da páxina principal
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

        if not check_user(id):
            return redirect(url_for("auth_bp.logout"))

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
                weather_data = None
                url = f"{config.FASTAPI_URL}/external-apis/current_weather"

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

                # Recollo todos os niveis de alerxias

                url = f"{config.FASTAPI_URL}/external-apis/current_pollen"

                response = requests.post(
                    url,
                    json=coordinates,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": config.API_KEY,
                    },
                )

                if response.status_code == 200:
                    pollen_levels = response.json()

                    user_allergies = get_pollen_names_by_user(id)

                    niveis_correspondentes = []

                    if pollen_levels is not None:
                        for allergy in user_allergies:
                            niveis_correspondentes.append(
                                [allergy[1], pollen_levels[allergy[0].lower()]]
                            )

                    if weather_data and niveis_correspondentes:
                        locations_info.append(
                            [
                                simplify_location(location),
                                get_userlog_by_loc(location),
                                weather_data,
                                niveis_correspondentes,
                            ]
                        )
                    else:
                        raise Exception("Problema devolvendo a resposta")

        get_pollen_names_by_user(id_user)

        return render_template(
            "index.html",
            locations=locations_info,
            is_admin=is_admin,
            name=name,
        )
    else:
        return redirect(url_for("auth_bp.logout"))


@bp.route("/get_session_location")
@login_required
def get_session_location():
    """
    Devolve a localización a partir da información almacenada na sesión.
    """

    location = session.get("user_location")

    return jsonify({"location": location})


@bp.route("/set_location", methods=["POST"])
@login_required
def set_location():
    """
    Garda a localización do usuario na sesión.
    """

    data = request.get_json()
    latitude = data["latitude"]
    longitude = data["longitude"]
    session["user_location"] = {"lat": latitude, "lng": longitude}

    return jsonify({"message": "Location saved!"})
