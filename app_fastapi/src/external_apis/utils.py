"""Funcións útiles para traballar con APIs externas"""

def get_pollen_level_description(value):
    """
    Devolve unha descrición do nivel de pole baseado no valor dado.

    Args:
        value: Nivel de pole. Integral ou None

    Returns:
        str: Descrición
    """
    if value is None:
        return "Sen datos"
    elif value <= 10:
        return "Baixo"
    elif value <= 30:
        return "Moderado"
    elif value <= 50:
        return "Alto"
    else:
        return "Moi alto"
