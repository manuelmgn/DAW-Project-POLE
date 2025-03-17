"""Rutas para os rexistros de usuario"""

from flask import (
    Blueprint,
    json,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
import requests
from utils.utils import call_api_key, login_required
from forms.forms import UserLogForm
from config.config import Config

log_bp = Blueprint("log_bp", __name__)
config = Config()

# ==============================================================================
# GET
# ==============================================================================


# ------------------------------------------------------------------------------
# DEVOLVE OS REXISTROS DUN USUARIO
# ------------------------------------------------------------------------------


@log_bp.route("/userlogs", methods=["GET"])
@login_required
def get_userlogs_by_user():
    """
    Devolve os rexistros dun usuario
    """

    id_user = session.get("id_user")

    if id_user:

        response = call_api_key("userlogs", id_user)

        if response.status_code == 200:
            userlogs = response.json()
            return render_template("userlogs/show.html", userlogs=userlogs)
        else:
            return render_template("userlogs/show.html")

    return redirect(url_for("auth_bp.login"))


# ==============================================================================
# POST
# ==============================================================================


@log_bp.route("/userlogs/new", methods=["GET", "POST"])
@login_required
def new_userlog():
    """
    Crea un novo rexistro de usuario
    """

    id_user = session.get("id_user")

    form = UserLogForm()

    if request.method == "POST":
        if id_user:

            # Procesa as coordenadas e converteas a string
            coordinates_str = request.form.get("coordinates", "")

            if not coordinates_str:
                return render_template("userlogs/new.html", form=form)

            try:
                coordinates = json.loads(coordinates_str)
                if isinstance(coordinates, str):
                    coordinates = json.loads(coordinates)
            except Exception:
                coordinates = (
                    coordinates_str.strip("[]")
                    .replace('"', "")
                    .replace("'", "")
                    .split(",")
                )

            coordinates = [str(coord).strip() for coord in coordinates]

            localizacion = dict(
                name=request.form.get("location", ""), coordinates=coordinates
            )

            data = {
                "timestamp": request.form["timestamp"],
                "location": localizacion,
                "severity": int(request.form["severity"]),
                "user_id": id_user,
            }

            response = requests.post(
                f"{config.FASTAPI_URL}/userlogs/new-userlog/",
                json=json.loads(json.dumps(data, default=str)),
                headers={"x-api-key": config.API_KEY},
            )

            if response.status_code == 200:
                return redirect(url_for("log_bp.get_userlogs_by_user"))
            else:
                print(f"Erro {response.status_code}:\n{response.text}")
    return render_template("userlogs/new.html", form=form)
