"""Rutas de usuario"""

from datetime import datetime
from flask import (
    Blueprint,
    flash,
    json,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
import json
import requests
from utils.utils import call_api_key, get_pollen_types, login_required
from forms.forms import UpdateLocationsForm, UpdateUserForm
from config.config import Config

user_bp = Blueprint("user_bp", __name__)
config = Config()

# ==============================================================================
# CRUD USER
# ==============================================================================

# ------------------------------------------------------------------------------
# MOSTRAR DATOS DE USUARIO
# ------------------------------------------------------------------------------


@user_bp.route("/user", methods=["GET"])
@login_required
def show_user():
    """
    Mostra os datos do usuario.
    """

    id_user = session.get("id_user")

    if id_user:
        response = call_api_key("user", id_user)

        if response.status_code == 200:
            response = requests.get(
                f"{config.FASTAPI_URL}/user/{id_user}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": config.API_KEY,
                },
            )
            user = response.json()

            return render_template("user/view.html", user=user)
        else:
            return redirect(url_for("auth_bp.login"))

    else:
        return redirect(url_for("auth_bp.login"))


# ------------------------------------------------------------------------------
# ACTUALIZAR USUARIO
# ------------------------------------------------------------------------------


@user_bp.route("/user/update", methods=["GET", "POST"])
@login_required
def update_user():
    """
    Actualiza os datos do usuario.
    """

    id_user = session.get("id_user")
    form = UpdateUserForm()

    pollens = get_pollen_types()

    if not id_user:
        return redirect(url_for("auth_bp.login"))

    try:
        response = requests.get(
            f"{config.FASTAPI_URL}/user/{id_user}",
            headers={
                "Content-Type": "application/json",
                "x-api-key": config.API_KEY,
            },
        )

        if response.status_code != 200:
            flash("Non se puido encontrar información do usuario", "error")
            return redirect(url_for("user_bp.show_user"))

        user_to_update = response.json()

        if request.method == "GET":

            form.name.data = user_to_update["name"]
            form.lastname.data = user_to_update["lastname"]
            form.email.data = user_to_update["email"]
            form.birthdate.data = (
                datetime.strptime(
                    user_to_update["birthdate"], "%Y-%m-%d"
                ).date()
                if user_to_update["birthdate"]
                else None
            )

            location = user_to_update.get("location", {})
            form.location.data = location.get("name", "")
            form.coordinates.data = location.get("coordinates", "")

            return render_template(
                "user/update.html",
                form=form,
                user_to_update=user_to_update,
            )

        if request.method == "POST":

            if form.validate_on_submit():
                try:
                    coordinates_str = request.form.get("coordinates", "")
                    try:
                        coordinates = json.loads(coordinates_str)
                        if isinstance(coordinates, str):
                            coordinates = json.loads(coordinates)
                    except Exception:
                        coordinates = (
                            coordinates_str.strip("[]")
                            .replace('"', "")
                            .split(",")
                        )

                    coordinates = [str(coord).strip() for coord in coordinates]

                    localizacion = {
                        "name": request.form.get("location", ""),
                        "coordinates": coordinates,
                    }

                    data = {
                        "name": request.form.get("name"),
                        "lastname": request.form.get("lastname"),
                        "email": request.form.get("email"),
                        "birthdate": request.form.get("birthdate"),
                        "location": localizacion,
                    }

                    response = requests.put(
                        f"{config.FASTAPI_URL}/user/{id_user}",
                        json=data,
                        headers={
                            "Content-Type": "application/json",
                            "x-api-key": config.API_KEY,
                        },
                    )

                    if response.status_code == 200:
                        flash("Usuario actualizado con éxito", "success")
                        session["location"] = localizacion
                        session["name"] = data["name"]
                        session["lastname"] = data["lastname"]
                        session["email"] = data["email"]
                        session["birthdate"] = data["birthdate"]
                        return redirect(url_for("user_bp.show_user"))
                    else:
                        error = (
                            json.loads(response.text)
                            if response.text
                            else "Erro"
                        )
                        return render_template(
                            "user/update.html",
                            form=form,
                        )

                except Exception as e:
                    error_message = f"Erro na actualización: {str(e)}\nDatos: {json.dumps(data, indent=2)}"
                    return render_template(
                        "user/view.html", form=form, error=error_message
                    )
            else:
                print("Erros na validación do formulario:")
                for field, errors in form.errors.items():
                    print(f"{field}: {errors}")
                return render_template("user/update.html", form=form)

    except Exception as e:
        flash(f"Erro inesperado: {str(e)}", "error")
        return redirect(url_for("user_bp.show_user"))

    return redirect(url_for("auth_bp.login"))


# ------------------------------------------------------------------------------
# BORRAR USUARIO
# ------------------------------------------------------------------------------


@user_bp.route("/user/delete", methods=["GET"])
@login_required
def delete_user_itself():
    """
    Borra o usuario (por si mesmo)
    """

    id_user = session.get("id_user")

    if id_user:
        # Comprobamos se existe o usuario
        response = call_api_key("user", id_user)
        if response.status_code == 200:
            # Chamada para borrar
            delete_response = requests.delete(
                f"{config.FASTAPI_URL}/user/{id_user}",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": config.API_KEY,
                },
            )

            if delete_response.status_code == 204:
                session.pop("id_user", None)
                flash("Conta borrada correctamente.", "success")
            else:
                flash(
                    "Erro no borrado da conta. Volve tentalo.",
                    "error",
                )
        else:
            flash("Usuario non encontrado.", "error")

    return redirect(url_for("auth_bp.register"))


# ==============================================================================
# OUTRAS RUTAS USUARIO
# ==============================================================================


@user_bp.route("/user/update/config/locations", methods=["GET", "POST"])
@login_required
def update_user_locations():
    """
    Actualiza as localizacións segundarias do usuario.
    """

    id_user = session.get("id_user")

    form = UpdateLocationsForm()

    if request.method == "POST":
        try:
            # Procesa as coordenadas e converteas a string
            coordinates_str = request.form.get("coordinates", "")

            try:
                # Converto as coordenadas a string
                coordinates = json.loads(coordinates_str)
                if isinstance(coordinates, str):
                    coordinates = json.loads(coordinates)
            except Exception:
                coordinates = (
                    coordinates_str.strip("[]").replace('"', "").split(",")
                )

            coordinates = [str(coord).strip() for coord in coordinates]

            # Creo a localización
            location = {
                "name": request.form.get("location", ""),
                "coordinates": coordinates,
            }

            # Prepara datos para enviar á API
            data = [location]

            # Chama a API
            response = requests.post(
                f"{config.FASTAPI_URL}/user/{id_user}/config/locations",
                json=data,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": config.API_KEY,
                },
            )

            if response.status_code == 200:
                flash(
                    "Localización secundaria actualizada!",
                    "success",
                )
                session["config"].get("fav_locations", "")[0] = location
                return redirect(url_for("user_profile"))
            else:
                error_message = response.json().get(
                    "detail", "Erro descoñecido"
                )
                flash(
                    f"Erro ao actualizar a localización: {error_message}",
                    "error",
                )
                return render_template(
                    "user/configlocations.html", form=form, error=error_message
                )
        except:
            print("Erro")

    return render_template("user/configlocations.html", form=form)
