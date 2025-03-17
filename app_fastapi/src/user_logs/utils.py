"""Funcións útiles para manexar os logs de usuario"""

import math


def haversine_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    ESTA FUNCIÓN FOI XERADA COMPLETAMENTE CON INTELIXENCIA ARTIFICIAL

    Calcula a distancia entre dúas coordenadas en km

    Args:
        lat1 (float): Latitude do punto 1.
        lon1 (float): Lonxitude do punto 1.
        lat2 (float): Latitude do punto 2.
        lon2 (float): Lonxitude do punto 2.

    Returns:
        float: Distancia entre os dous puntos en km.
    """

    R = 6371.0  # Radio de la Tierra en kilómetros

    # Convertir a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Diferencias de coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
