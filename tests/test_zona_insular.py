"""Pruebas de aceptación para la zona insular de San Andrés (Fase 7)."""

import pytest

from src.calculadora import calc


def test_insular_aplica_recargo_del_70_por_ciento():
    # 3 kg inicia el tramo 2: 9.000 * 1,70 = 15.300.
    assert calc(3, "insular", "normal", 1) == 15300


@pytest.mark.parametrize("cupon", [None, ""])
def test_insular_permite_sin_cupon(cupon):
    assert calc(3, "insular", "normal", 1, cup=cupon) == 15300


@pytest.mark.parametrize("cupon", ["ENVIO10", "CUPON-INEXISTENTE"])
def test_insular_rechaza_cualquier_cupon_proporcionado(cupon):
    # El tipo de excepción no está fijado por el requisito; ValueError es la
    # decisión técnica adoptada para una combinación zona/cupón no admitida.
    with pytest.raises(ValueError, match="no admite cupones"):
        calc(3, "insular", "normal", 1, cup=cupon)


def test_insular_aplica_descuento_frecuente():
    # 15.300 * 0,95 = 14.535; al centenar más cercano = 14.500.
    assert calc(3, "insular", "frecuente", 1) == 14500


def test_insular_aplica_descuento_vip():
    # 15.300 * 0,85 = 13.005; redondeado = 13.000.
    assert calc(3, "insular", "vip", 1) == 13000


def test_insular_aplica_fin_de_semana_antes_del_descuento_vip():
    # (9.000 * 1,70 + 2.000) * 0,85 = 14.705; redondeado = 14.700.
    assert calc(3, "insular", "vip", 7) == 14700


def test_insular_aplica_fin_de_semana_antes_del_descuento_frecuente():
    # (9.000 * 1,70 + 2.000) * 0,95 = 16.435; redondeado = 16.400.
    assert calc(3, "insular", "frecuente", 6) == 16400


def test_insular_conserva_validacion_general_de_peso():
    with pytest.raises(ValueError, match="peso"):
        calc(0, "insular", "normal", 1)


def test_insular_conserva_validacion_general_de_dia():
    with pytest.raises(ValueError, match="día"):
        calc(3, "insular", "normal", 8)


def test_otras_zonas_ignoran_cupon_desconocido_por_r7():
    # Paridad F=2: el cupón no reconocido se ignora fuera de zona insular.
    assert calc(3, "urbana", "normal", 1, cup="CUPON-INEXISTENTE") == 9000



@pytest.mark.parametrize(
    ("peso", "zona", "cliente", "dia", "cupon", "esperado"),
    [
        pytest.param(
            11, "rural", "frecuente", 1, "ENVIO10", 10100, id="INS-13"
        ),
        pytest.param(
            50, "rural", "vip", 6, None, 43500, id="INS-14"
        ),
        pytest.param(
            11, "nacional", "frecuente", 1, None, 14000, id="INS-15"
        ),
        pytest.param(
            50, "nacional", "normal", 7, "ENVIO10", 57200, id="INS-16"
        ),
        pytest.param(
            11, "insular", "frecuente", 1, None, 15800, id="INS-17"
        ),
        pytest.param(
            50, "insular", "vip", 7, None, 60900, id="INS-18"
        ),
    ],
)
def test_recargos_zonales_sobre_tramo_proporcional(
    peso, zona, cliente, dia, cupon, esperado
):
    """Comprueba recargos >10 kg, PMAX, calendario, descuentos y redondeo."""
    assert calc(peso, zona, cliente, dia, cup=cupon) == esperado
