"""Esquemas Pydantic para os usuarios"""

from datetime import date
import json
from typing import List
from pydantic import BaseModel, EmailStr


class Location(BaseModel):
    """Modelo de localización"""

    name: str
    coordinates: List[str]

    def to_dict(self):
        return {"name": self.name, "coordinates": self.coordinates}


class Config(BaseModel):
    """Modelo de configuración de cara usuario"""

    fav_locations: list[Location] = []

    def to_dict(self):
        return {
            "fav_locations": self.fav_locations,
        }


class UserBase(BaseModel):
    """Modelo base de usuario"""

    name: str
    lastname: str
    email: EmailStr
    location: Location
    birthdate: date


class UserCreate(UserBase):
    """Modelo ampliado para crear un usuario novo"""

    username: str
    password: str
    pollen_allergies: list[int] = []


class UserResponse(UserBase):
    """Modelo ampliado para devolver máis info"""

    id_user: int
    name: str
    lastname: str
    email: EmailStr
    username: str
    location: Location
    birthdate: date
    role: str
    enabled: bool
    config: Config
    # allergies: List[PollenResponse] = []

    class Config:
        from_attributes = True


class UserCompleteEdition(UserBase):
    """Modelo ampliado para editar completamente un usuario"""

    username: str
    password: str
    role: str
    enabled: bool


class UserNameEdition(BaseModel):
    """Modelo ampliado para editar o nome dun usuario"""

    name: str
    lastname: str


class UserPassEdition(BaseModel):
    """Modelo ampliado para editar o contrasinal dun usuario"""

    password: str


class UserLocEdition(BaseModel):
    """Modelo ampliado para editar a localización dun usuario"""

    location: Location


class UserallergiesEdition(BaseModel):
    """Modelo ampliado para editar os tipos de alerxia dun usuario"""

    pollen_allergies: list[int] = []


class UserConfig(BaseModel):
    """Modelo ampliado para incluir opcións de configuración"""

    config: Config
