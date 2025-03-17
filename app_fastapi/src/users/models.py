"""Modelos de usuarios na base de datos"""

from sqlalchemy import (
    JSON,
    Column,
    Integer,
    String,
    Boolean,
    Date,
)
from sqlalchemy.orm import relationship
from database.base import Base


class User(Base):
    """Clase que representa un usuario"""

    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    location = Column(JSON, nullable=False)
    role = Column(String, default="basic", nullable=False)
    enabled = Column(Boolean, default=True)

    user_logs = relationship("UserLog", back_populates="user")

    config = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<User(name={self.id_user}, email={self.username})>"