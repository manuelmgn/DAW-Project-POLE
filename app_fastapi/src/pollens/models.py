"""Modelos para os tipos de pole"""

from enum import Enum
from sqlalchemy import Column, Integer, String

from database.base import Base


class Pollen(Base):
    """Clase Pole"""

    __tablename__ = "pollens"

    id_pollen = Column(Integer, primary_key=True, index=True)
    pollen_name = Column(String, nullable=False)
    pollen_gal = Column(String, nullable=False)


class PollenType(str, Enum):
    """Enumeración dos tipos de pole"""

    RAGWEED = "Ambrosía"
    ALDER = "Ameneiro"
    MUGWORT = "Artemisa"
    BIRCH = "Bidueiro"
    GRASS = "Herba"
    OLIVE = "Oliveira"
