"""Rutas de autenticación e creación de usuarios"""

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

from utils.utils import get_pollen_types, login_required
from forms.forms import RegisterForm
from config.config import Config
import requests


auth_bp = Blueprint("auth_bp", __name__)
config = Config()

# ------------------------------------------------------------------------------
# REXISTRO
# ------------------------------------------------------------------------------


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Rexistra un novo usuario.
    """

    # Nova instancia da clase do formulario de rexistro
    form = RegisterForm()
    # Importo os tipos de pole e os asigno ao campo
    pollens = get_pollen_types()

    form.pollen_allergies.choices = [
        (pollen["id_pollen"], pollen["pollen_gal"]) for pollen in pollens
    ]

    if request.method == "POST":
        if form.validate_on_submit():
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

                localizacion = {
                    "name": request.form.get("location", ""),
                    "coordinates": coordinates,
                }

                data = {
                    "name": request.form.get("name", ""),
                    "lastname": request.form.get("lastname", ""),
                    "email": request.form.get("email", ""),
                    "username": request.form.get("username", ""),
                    "password": request.form.get("password", ""),
                    "birthdate": request.form.get("birthdate", ""),
                    "location": localizacion,
                    "pollen_allergies": request.form.getlist(
                        "pollen_allergies"
                    ),
                }


                response = requests.post(
                    f"{config.FASTAPI_URL}/user/",
                    json=data,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": config.API_KEY,
                    },
                )

                if response.status_code == 200:
                    print("Rexistro realizado con éxito")
                    return redirect(url_for("auth_bp.login"))
                else:
                    error = f"Erro na resposta do servidor: {response.status_code} - {response.text}"

                    return render_template(
                        "auth/register.html",
                        form=form,
                        error=json.loads(response.text),
                    )

            except Exception as e:
                error = f"Erro no rexistro: {str(e)}\nDatos: {json.dumps(data, indent=2)}"
                print(error)
                return render_template(
                    "auth/register.html", form=form, error=error
                )

        else:
            print(form.errors)
            return render_template("auth/register.html", form=form)

    return render_template("auth/register.html", form=form)


# ------------------------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------------------------


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Iniciar sesión.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            response = requests.post(
                f"{config.FASTAPI_URL}/auth/login",
                json={"username": username, "password": password},
                headers={"x-api-key": config.API_KEY},
            )
            if response.status_code == 200:
                user_data = response.json()
                session["id_user"] = user_data["id_user"]
                session["username"] = user_data["username"]
                session["name"] = user_data["name"]
                session["location"] = user_data["location"]
                session["config"] = user_data["config"]

                if user_data["role"] == "admin":
                    session["admin"] = True
                else:
                    session["admin"] = False
                return redirect(url_for("main.index"))
            else:
                flash("Nome de usuario ou contrasinal inválidos", "danger")

        except requests.exceptions.RequestException as e:
            flash("Erro ao estabelecer a conexión co servidor.", "danger")

    return render_template("auth/login.html")


# ------------------------------------------------------------------------------
# LOGOUT
# ------------------------------------------------------------------------------


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Pecha a sesión do usuario.
    """

    # Limpamos os datos da sesión
    session.clear()
    # Alternativa_ session.pop('usuario', None)
    flash("👃 Chao!", "info")
    
    return redirect(url_for("main.index"))
