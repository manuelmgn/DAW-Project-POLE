"""Modelos Pydantic para importar os esquemas"""

from datetime import datetime
from typing import List
import json
from pydantic import BaseModel


class Location(BaseModel):
    """Modelo para a localización"""

    name: str
    coordinates: List[str]

    class Config:
        json_encoders = {datetime: str}

    def dict(self, *args, **kwargs):
        return {"name": self.name, "coordinates": self.coordinates}

    def json(self):
        return json.dumps(self.dict())


class UserLogBase(BaseModel):
    """Clase base para rexistros de usuario"""

    severity: int
    timestamp: datetime
    location: Location

    def dict(self):
        return {
            "severity": self.severity,
            "timestamp": self.timestamp,
            "location": self.location.dict() if self.location else None,
        }


class UserLogCreate(UserLogBase):
    """Clase para crear rexistros de usuarios"""

    user_id: int


class UserLogResponse(UserLogBase):
    """Modelo ampliado para devolver máis info"""

    id_userlog: int
    severity: int
    timestamp: datetime
    location: Location
    user_id: int

    class Config:
        from_attributes = True
