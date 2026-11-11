"""Automatización de BB-01 a BB-41 contra los requisitos R1–R8.

Los valores esperados proceden de docs/03_caja_negra.md. Algunas aserciones
fallarán contra envios.py heredado; no se sustituyen por los resultados del legado.
"""
import pytest

from envios import calc


# Marcador interno: R2 exige que se lance un error pero no especifica su clase.
R2_ERROR = object()

CASES = [
    pytest.param((0, "urbana", "normal", 1, None), ValueError, id="BB-01"),
    pytest.param((0.001, "urbana", "normal", 1, None), 6000, id="BB-02"),
    pytest.param((2.999, "urbana", "normal", 1, None), 6000, id="BB-03"),
    pytest.param((3, "urbana", "normal", 1, None), 9000, id="BB-04"),
    pytest.param((3.001, "urbana", "normal", 1, None), 9000, id="BB-05"),
    pytest.param((9.999, "urbana", "normal", 1, None), 9000, id="BB-06"),
    pytest.param((10, "urbana", "normal", 1, None), 9000, id="BB-07"),
    pytest.param((10.001, "urbana", "normal", 1, None), 9000, id="BB-08"),
    pytest.param((49.999, "urbana", "normal", 1, None), 41000, id="BB-09"),
    pytest.param((50, "urbana", "normal", 1, None), 41000, id="BB-10"),
    pytest.param((50.001, "urbana", "normal", 1, None), ValueError, id="BB-11"),
    pytest.param((3, "urbana", "normal", 0, None), R2_ERROR, id="BB-12"),
    pytest.param((3, "urbana", "normal", 1, None), 9000, id="BB-13"),
    pytest.param((3, "urbana", "normal", 7, None), 11000, id="BB-14"),
    pytest.param((3, "urbana", "normal", 8, None), R2_ERROR, id="BB-15"),
    pytest.param((3, "urbana", "normal", 1, None), 9000, id="BB-16"),
    pytest.param((3, "rural", "normal", 1, None), 10800, id="BB-17"),
    pytest.param((3, "nacional", "normal", 1, None), 13500, id="BB-18"),
    pytest.param((3, "costera", "normal", 1, None), R2_ERROR, id="BB-19"),
    pytest.param((3, "urbana", "normal", 1.5, None), R2_ERROR, id="BB-20"),
    pytest.param((3, "urbana", "normal", 6, None), 11000, id="BB-21"),
    pytest.param((3, "urbana", "normal", 1, None), 9000, id="BB-22"),
    pytest.param((3, "urbana", "normal", 1, "X"), 9000, id="BB-23"),
    pytest.param((3, "urbana", "normal", 1, "ENVIO10"), 8100, id="BB-24"),
    pytest.param((3, "urbana", "normal", 6, None), 11000, id="BB-25"),
    pytest.param((3, "urbana", "normal", 6, "X"), 11000, id="BB-26"),
    pytest.param((3, "urbana", "normal", 6, "ENVIO10"), 9900, id="BB-27"),
    pytest.param((3, "urbana", "frecuente", 1, None), 8600, id="BB-28"),
    pytest.param((3, "urbana", "frecuente", 1, "X"), 8600, id="BB-29"),
    pytest.param((3, "urbana", "frecuente", 1, "ENVIO10"), 7700, id="BB-30"),
    pytest.param((3, "urbana", "frecuente", 6, None), 10500, id="BB-31"),
    pytest.param((3, "urbana", "frecuente", 6, "X"), 10500, id="BB-32"),
    pytest.param((3, "urbana", "frecuente", 6, "ENVIO10"), 9400, id="BB-33"),
    pytest.param((3, "urbana", "vip", 1, None), 7700, id="BB-34"),
    pytest.param((3, "urbana", "vip", 1, "X"), 7700, id="BB-35"),
    pytest.param((3, "urbana", "vip", 1, "ENVIO10"), 6900, id="BB-36"),
    pytest.param((3, "urbana", "vip", 6, None), 9400, id="BB-37"),
    pytest.param((3, "urbana", "vip", 6, "X"), 9400, id="BB-38"),
    pytest.param((3, "urbana", "vip", 6, "ENVIO10"), 8400, id="BB-39"),
    pytest.param((10.0625, "urbana", "normal", 1, None), 9100, id="BB-40"),
    pytest.param((0.001, "urbana", "vip", 1, "ENVIO10"), 5000, id="BB-41"),
]


@pytest.mark.parametrize(("args", "expected"), CASES)
def test_caja_negra_requisitos_r1_a_r8(args, expected, request):
    """Cada ID visible corresponde a un caso diseñado en la Parte 3."""
    case_id = request.node.callspec.id
    if expected is ValueError:
        with pytest.raises(ValueError):
            calc(*args)
        return
    if expected is R2_ERROR:
        # R2 solicita error, pero no prescribe una clase concreta.
        try:
            actual = calc(*args)
        except Exception:
            return
        pytest.fail(
            f"{case_id}: R2 esperaba una excepción; el código heredado retornó {actual}"
        )

    actual = calc(*args)
    assert actual == expected, (
        f"{case_id}: esperado por R1–R8={expected}, observado en legado={actual}"
    )
