from PyQt5.QtGui import QColor
from datetime import datetime

def iso_to_de(iso_date: str) -> str:
    """
    Wandelt ein ISO-Datum (YYYY-MM-DD) in deutsches Format (DD.MM.YYYY)
    """
    try:
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return ""

def de_to_iso(de_date: str) -> str:
    """
    Wandelt ein deutsches Datum (DD.MM.YYYY) in ISO-Format (YYYY-MM-DD)
    """
    try:
        dt = datetime.strptime(de_date, "%d.%m.%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return ""

def hex_to_qcolor(hex_color: str) -> QColor:
    """
    Wandelt einen HEX-String (#RRGGBB) in ein QColor-Objekt
    """
    return QColor(hex_color)

def qcolor_to_hex(color: QColor) -> str:
    """
    Wandelt ein QColor-Objekt in einen HEX-String (#RRGGBB)
    """
    return color.name()
