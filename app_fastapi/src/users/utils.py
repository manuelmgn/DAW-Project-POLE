"""Funcións útiles para o traballo con usuarios en FastAPI"""

from sqlalchemy.orm import Session

from users.models import User
from database.relations import UserPollens
from security import get_password_hash
from .models import User


# ==============================================================================
# BASE DE DATOS
# ==============================================================================

# ------------------------------------------------------------------------------
# FUNCIÓN DE CREADO DE ADMIN
# ------------------------------------------------------------------------------

def load_admin(db: Session):
    """
    Función para cargar un usuario administrador.

    Args:
        db (Session): Sesión da base de datos.
    
    Raises:
        Exception: Se hai algún erro ao cargar o usuario.
    """
    try:
        # Verificar se xa existe este admin
        existing_users = db.query(User).count()

        if existing_users == 0:
            hashed_password = get_password_hash("123123")

            admin = User(
                name="Administrador",
                lastname="Sistema",
                email="admin@pole.gal",
                location={"name": "Cuntis, Caldas, Pontevedra, Galiza, Espanha", "coordinates": ["42.6353362", "-8.5617942"]},
                birthdate="2000-01-01",
                username="admin",
                password=hashed_password,
                role="admin",
                enabled=True,
                config={"fav_locations": [{"name": "Cuntis, Caldas, Pontevedra, Galiza, Espanha", "coordinates": ["42.6353362", "-8.5617942"]}]},
            )

            db.add(admin)
            db.commit()
            db.refresh(admin)

    except Exception as e:
        print(f"Erro ao cargar o usuario administrador: {e}")
        db.rollback()

    try:
        admin = db.query(User).filter(User.username=="admin").first()
        id_admin = getattr(admin, 'id_user')
        alerxias_admin = db.query(UserPollens).filter(UserPollens.user_id==id_admin).first()
        if admin:
            if not alerxias_admin:
                admin_pollens = UserPollens(
                    user_id=id_admin,
                    pollen_id=1,
                )
                db.add(admin_pollens)
                db.commit()
    
    except Exception as e:
        print(f"Erro ao cargar as alerxias do administrador: {e}")
        db.rollback()

    finally:
        db.close()