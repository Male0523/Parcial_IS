"""Comprobaciones defensivas adicionales de la calculadora refactorizada."""

import pytest

from src.calculadora import calc


@pytest.mark.parametrize("peso", ["abc", None, True])
def test_rechaza_peso_no_numerico(peso):
    with pytest.raises(ValueError):
        calc(peso, "urbana", "normal", 1)


@pytest.mark.parametrize("peso", [float("nan"), float("inf")])
def test_rechaza_peso_no_finito(peso):
    with pytest.raises(ValueError):
        calc(peso, "urbana", "normal", 1)


def test_rechaza_dia_booleano():
    # bool hereda de int en Python, pero el requisito pide un número de día entero.
    with pytest.raises(ValueError):
        calc(3, "urbana", "normal", True)


def test_rechaza_zona_de_tipo_no_admitido():
    with pytest.raises(ValueError):
        calc(3, None, "normal", 1)
