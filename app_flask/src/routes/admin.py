"""Rutas de administración"""

from flask import (
    Blueprint,
    flash,
    render_template,
    redirect,
    session,
)
import requests
from utils.utils import call_api_key, login_required
from config.config import Config

admin_bp = Blueprint("admin_bp", __name__)
config = Config()


# ==============================================================================
# CRUD DE ADMINISTRADOR
# ==============================================================================

# ------------------------------------------------------------------------------
# VER
# ------------------------------------------------------------------------------

@admin_bp.route("/admin/users", methods=["GET"])
@login_required
def manage_users():
    """
    Mostra a páxina de administración de usuarios
    """
    if not session.get("admin"):
        return redirect("/")

    response = requests.get(
        f"{config.FASTAPI_URL}/user/",
        headers={
            "Content-Type": "application/json",
            "x-api-key": config.API_KEY,
        },
    )

    if response.status_code == 200:
        usuarios = response.json()
    else:
        error = f"Erro na resposta do servidor: {response.status_code} - {response.text}"
        print(error)

    return render_template("/admin/users-admin.html", usuarios=usuarios)


# ------------------------------------------------------------------------------
# BORRAR USUARIO
# ------------------------------------------------------------------------------


@admin_bp.route("/admin/users/delete/<int:id>", methods=["GET"])
@login_required
def delete_user(id):
    """
    Borra un usuario, dado o seu id
    """

    if not session.get("admin"):
        return redirect("/")

    # Comprobamos se existe o usuario
    response = call_api_key("user", id)
    if response.status_code == 200:

        delete_response = requests.delete(
            f"{config.FASTAPI_URL}/user/{id}",
            headers={
                "Content-Type": "application/json",
                "x-api-key": config.API_KEY,
            },
        )

        if delete_response.status_code == 204:
            session.pop("id_user", None)
            flash("Conta borrada correctamente.", "success")
        else:
            flash("Erro ao borrar o usuario. Téntao de novo.", "error")
    else:
        flash("Usuario non encontrado.", "error")

    return redirect("/admin/users")


# ------------------------------------------------------------------------------
# DESACTIVAR
# ------------------------------------------------------------------------------

@admin_bp.route("/admin/users/deactivate/<int:id>", methods=["GET"])
@login_required
def deactivate_user(id):
    """
    Activa ou desactiva un usuario, dado o seu id
    """

    if not session.get("admin"):
        return redirect("/")

    response = call_api_key("user", id)

    if response.status_code == 200:

        deac_response = requests.put(
            f"{config.FASTAPI_URL}/user/deactivate/{id}",
            headers={
                "Content-Type": "application/json",
                "x-api-key": config.API_KEY,
            },
        )

        if deac_response.status_code == 204:
            session.pop("id_user", None)
            flash("Conta (des)activada correctamente.", "success")
        else:
            flash("Erro ao (des)activar o usuario. Téntao de novo.", "error")
    else:
        flash("Usuario non encontrado.", "error")

    return redirect("/admin/users")
