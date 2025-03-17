# Táboa intermedia para a relación usuarios-tipos de pole
from pydantic import ConfigDict
from sqlalchemy import Column, ForeignKey, Integer, Table

from database.base import Base
from users.models import User
from pollens.models import Pollen


class UserPollens(Base):
    """
    Clase para a táboa intermedia entre usuarios e tipos de pole.
    """

    __tablename__ = "user_pollens"

    user_id = Column(
        Integer, ForeignKey("users.id_user"), primary_key=True, nullable=False
    )
    pollen_id = Column(
        Integer,
        ForeignKey("pollens.id_pollen"),
        primary_key=True,
        nullable=False,
    )

    def __init__(self, user_id: int, pollen_id: int):
        self.user_id = user_id
        self.pollen_id = pollen_id
