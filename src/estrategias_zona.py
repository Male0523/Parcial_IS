"""Estrategias concretas para aplicar el recargo de cada zona."""

from decimal import Decimal
from typing import Protocol

from .configuracion import RECARGO_NACIONAL, RECARGO_RURAL, UNO


class EstrategiaZona(Protocol):
    """Interfaz común para calcular el subtotal correspondiente a una zona."""

    def aplicar(self, subtotal: Decimal) -> Decimal:
        ...


class ZonaUrbana:
    """La zona urbana no modifica la tarifa."""

    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal


class ZonaRural:
    """La zona rural aplica el recargo personalizado del 20 %."""

    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal * (UNO + RECARGO_RURAL)


class ZonaNacional:
    """La zona nacional aplica el recargo personalizado del 50 %."""

    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal * (UNO + RECARGO_NACIONAL)


ESTRATEGIAS_ZONA: dict[str, EstrategiaZona] = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}


def obtener_estrategia_zona(zona: str) -> EstrategiaZona:
    """Devuelve la estrategia de zona o rechaza una zona no admitida."""
    try:
        return ESTRATEGIAS_ZONA[zona]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"zona no válida: {zona!r}") from exc
