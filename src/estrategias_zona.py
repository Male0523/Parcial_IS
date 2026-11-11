"""Estrategias concretas para aplicar el recargo de cada zona."""

from decimal import Decimal
from typing import Protocol

from .configuracion import RECARGO_INSULAR, RECARGO_NACIONAL, RECARGO_RURAL, UNO


class EstrategiaZona(Protocol):
    """Interfaz común para calcular tarifa y política de cupones por zona."""

    permite_cupones: bool

    def aplicar(self, subtotal: Decimal) -> Decimal:
        ...


class ZonaUrbana:
    """La zona urbana no modifica la tarifa."""

    permite_cupones = True

    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal


class ZonaRural:
    """La zona rural aplica el recargo personalizado del 20 %."""

    permite_cupones = True

    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal * (UNO + RECARGO_RURAL)


class ZonaNacional:
    """La zona nacional aplica el recargo personalizado del 50 %."""

    permite_cupones = True

    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal * (UNO + RECARGO_NACIONAL)


class ZonaInsular:
    """San Andrés aplica un recargo del 70 % y no admite cupones."""

    permite_cupones = False

    def aplicar(self, subtotal: Decimal) -> Decimal:
        return subtotal * (UNO + RECARGO_INSULAR)


ESTRATEGIAS_ZONA: dict[str, EstrategiaZona] = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
    "insular": ZonaInsular(),
}


def obtener_estrategia_zona(zona: str) -> EstrategiaZona:
    """Devuelve la estrategia de zona o rechaza una zona no admitida."""
    try:
        return ESTRATEGIAS_ZONA[zona]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"zona no válida: {zona!r}") from exc
