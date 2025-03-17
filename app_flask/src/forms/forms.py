from datetime import datetime
from flask import session
from flask_wtf import FlaskForm
from pydantic import ValidationError
from wtforms import (
    DateField,
    DateTimeLocalField,
    EmailField,
    HiddenField,
    PasswordField,
    SelectMultipleField,
    StringField,
    SubmitField,
    RadioField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    EqualTo,
    Email,
    NumberRange,
    ValidationError,
)
from datetime import datetime, timedelta

# ==============================================================================
# AUTH
# ==============================================================================


# ------------------------------------------------------------------------------
# REGISTRO
# ------------------------------------------------------------------------------

class RegisterForm(FlaskForm):
    """
    Formulario de rexistro de usuario.
    """
    today = datetime.today()

    name = StringField("Nome", [InputRequired(), Length(min=2, max=50)])
    lastname = StringField(
        "Apelidos", [InputRequired(), Length(min=2, max=100)]
    )

    email = EmailField("Email", [InputRequired(), Email()])
    username = StringField(
        "Nome de usuario", [InputRequired(), Length(min=2, max=20)]
    )
    password = PasswordField(
        "Contrasinal", [InputRequired(), Length(min=6, max=100)]
    )
    confirm_password = PasswordField(
        "Confirmar contrasinal",
        [
            InputRequired(),
            EqualTo(
                "password",
                message="O contrasinal debe coincidir nos dous campos",
            ),
        ],
    )
    birthdate = DateField(
        "Data de nacemento", [InputRequired()], format="%Y-%m-%d"
    )
    pollen_allergies = SelectMultipleField(
        "Alerxias", validators=[InputRequired()]
    )
    location = StringField("Localización", [InputRequired()])
    coordinates = HiddenField(
        "Coordenadas",
        [
            InputRequired(
                message="A localización seleccionada produciu un problema. Tenta procurala doutro xeito"
            )
        ],
    )
    submit = SubmitField("Rexistrarse")

    def validate_birthdate(self, field):
        if field.data > datetime.now().date():
            raise ValidationError("A data de nacemento debe ser no pasado.")
        if field.data < datetime(1900, 1, 1).date():
            raise ValidationError(
                "A data de nacemento non pode ser antes de 1900."
            )
        eighteen_years_ago = datetime.now().date() - timedelta(days=18 * 365)
        if field.data > eighteen_years_ago:
            raise ValidationError("Debes ter polo menos 18 anos de idade.")


# ==============================================================================
# USER LOGS
# ==============================================================================


class UserLogForm(FlaskForm):
    """
    Formulario de rexistros de síntomas.
    """
    timestamp = DateTimeLocalField("Data e hora", [InputRequired()])
    severity = RadioField(
        "Intensidade dos síntomas",
        [InputRequired()],
        choices=[
            (1, "Sen síntomas"),
            (2, "Síntomas lixeiros e puntuais"),
            (3, "Síntomas frecuentes e lixeiros"),
            (4, "Síntomas fortes ou constantes"),
            (5, "Síntomas moi fortes"),
        ],
        default=3,
    )
    location = StringField("Localización", [InputRequired()])
    coordinates = HiddenField(
        "Coordenadas",
        [
            InputRequired(
                message="A localización seleccionada produciu un problema. Tenta procurala doutro xeito"
            )
        ],
    )
    user_id = HiddenField("User ID")
    submit = SubmitField("Rexistrar")

    def __init__(self, *args, **kwargs):
        super(UserLogForm, self).__init__(*args, **kwargs)
        self.timestamp.default = datetime.now()
        self.location.default = session.get("location", {}).get("name", "")
        self.coordinates.default = session.get("location", {}).get(
            "coordinates", ""
        )
        self.user_id.default = session.get("user_id")
        self.process()

    def validate_timestamp(self, field):
        today = datetime.now().date()
        seven_days_ago = today - timedelta(days=7)

        if field.data > today:
            raise ValidationError("A data e hora non pode ser no futuro.")
        if field.data < seven_days_ago:
            raise ValidationError(
                "A data e hora debe estar dentro dos últimos 7 días."
            )
        if field.data < datetime(1900, 1, 1).date():
            raise ValidationError("A data e hora non pode ser antes de 1900.")


# ==============================================================================
# USERS
# ==============================================================================


class UpdateUserForm(FlaskForm):
    """
    Formulario de actualización de usuario.
    """

    name = StringField("Nome", [InputRequired(), Length(min=2, max=50)])
    lastname = StringField(
        "Apelidos", [InputRequired(), Length(min=2, max=100)]
    )
    email = EmailField("Email", [InputRequired(), Email()])
    birthdate = DateField(
        "Data de nacemento",
        [InputRequired()],
        format="%Y-%m-%d",
    )
    location = StringField("Localización", [InputRequired()])
    coordinates = HiddenField(
        "Coordenadas",
        [
            InputRequired(
                message="A localización seleccionada produciu un problema. Tenta procurala doutro xeito"
            )
        ],
    )
    submit = SubmitField("Actualizar")

    def validate_birthdate(self, field):
        if field.data >= datetime.now().date():
            raise ValidationError("A data de nacemento debe ser no pasado.")
        if field.data < datetime(1900, 1, 1).date():
            raise ValidationError(
                "A data de nacemento non pode ser antes de 1900."
            )


class UpdateLocationsForm(FlaskForm):
    """
    Formulario de actualización de localizacións favoritas.
    """
    
    location = StringField("Localización 1")
    coordinates = HiddenField("Coordinates 1")
    # location2 = StringField("Localización 2",)
    # coordinates2 = HiddenField("Coordinates 2")
    # location3 = StringField("Localización 3")
    # coordinates3 = HiddenField("Coordinates 3")
    submit = SubmitField("Gardar")

    def __init__(self, *args, **kwargs):
        super(UpdateLocationsForm, self).__init__(*args, **kwargs)
        # self.location.default = session.get("location", {}).get("name", "")
        # self.coordinates.default = session.get("location", {}).get("coordinates", "")
        self.process()
