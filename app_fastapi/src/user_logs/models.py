"""Modelos da base de datos dos rexistros"""

from datetime import datetime
from sqlalchemy import JSON, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.base import Base


class UserLog(Base):
    """
    Clase que representa os rexistros das alerxias dos usuarios.

    Attributes:
        id_userlog (int): ID.
        timestamp (datetime): Data e hora na que é creado o rexistro.
        location (JSON): Localización na que se produce o sínstoma.
        severity (int): Intensidade dos síntomas.
        user_id (int): Chave secundaria que referencia ao usuario que fai o rexistro.
        user (User): Relación co modelo de User.
    """

    __tablename__ = "user_logs"

    id_userlog = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(JSON, nullable=False)
    severity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    user = relationship("User", back_populates="user_logs")
