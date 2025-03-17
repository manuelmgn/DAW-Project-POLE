"""Esquemas para os tipos de pole"""

from pydantic import BaseModel, ConfigDict


class PollenResponse(BaseModel):
    """
    Modelo para resposta de pole

    Attributes:
        id_pollen (int): Identificador único.
        pollen_name (str): Nome xenérico do pole.
        pollen_gal (str): Nome en galego.

    Config:
        model_config (ConfigDict): Configuración do modelo.
    """

    id_pollen: int
    pollen_name: str
    pollen_gal: str

    model_config = ConfigDict(from_attributes=True)
