"""Recorridos estructurales P01–P15 de la función calc heredada.

Estos asertos caracterizan rutas/salidas actuales para comprobar el flujo y la
cobertura. No convierten fallos del legado frente a R1–R8 en resultados válidos.
P01 usa una zona inválida solo para recorrer estructuralmente el else del
encadenamiento de zonas.
"""
import pytest

from envios import calc


PATHS = [
    pytest.param((11, "costera", "normal", 1, "X", False), 9800, None, id="P01"),
    pytest.param((-1, "urbana", "normal", 1, None, False), ValueError, None, id="P02"),
    pytest.param((51, "urbana", "normal", 1, None, False), ValueError, None, id="P03"),
    pytest.param((2, "urbana", "normal", 1, None, False), 6000, None, id="P04"),
    pytest.param((5, "urbana", "normal", 1, None, False), 9000, None, id="P05"),
    pytest.param((11, "urbana", "normal", 1, None, False), 9800, None, id="P06"),
    pytest.param((11, "rural", "normal", 1, None, False), 11700, None, id="P07"),
    pytest.param((11, "nacional", "normal", 1, None, False), 14700, None, id="P08"),
    pytest.param((11, "urbana", "normal", 7, None, False), 11800, None, id="P09"),
    pytest.param((11, "urbana", "frecuente", 1, None, False), 9300, None, id="P10"),
    pytest.param((11, "urbana", "vip", 1, None, False), 8300, None, id="P11"),
    pytest.param((2, "urbana", "normal", 1, "X", False), 6000, None, id="P12"),
    pytest.param((11, "urbana", "normal", 1, "ENVIO10", False), 8800, None, id="P13"),
    pytest.param((0.001, "urbana", "vip", 1, "ENVIO10", False), 5000, None, id="P14"),
    pytest.param((3, "urbana", "normal", 1, None, True), 6000, "costo: 6000\n", id="P15"),
]


@pytest.mark.parametrize(("args", "expected", "expected_stdout"), PATHS)
def test_camino_independiente_del_legado(args, expected, expected_stdout, request, capsys):
    """Verifica la ruta y caracterización del legado para el ID P correspondiente."""
    case_id = request.node.callspec.id

    if expected is ValueError:
        with pytest.raises(ValueError):
            calc(*args)
        captured = capsys.readouterr()
        assert captured.out == "", f"{case_id}: una excepción de peso no debe imprimir"
        return

    actual = calc(*args)
    assert actual == expected, (
        f"{case_id}: esperado en caracterización estructural={expected}, legado={actual}"
    )
    captured = capsys.readouterr()
    assert captured.out == (expected_stdout or ""), f"{case_id}: salida de consola inesperada"
