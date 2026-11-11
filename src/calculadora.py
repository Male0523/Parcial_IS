"""Cálculo de costos de envío con validaciones y contexto de zona."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from .configuracion import (
    CERO,
    CODIGO_CUPON,
    COSTO_MINIMO,
    COSTO_POR_KG_ADICIONAL,
    DESCUENTO_CUPON,
    DESCUENTO_FRECUENTE,
    DESCUENTO_VIP,
    DIAS_FIN_SEMANA,
    LIMITE_TRAMO_1,
    LIMITE_TRAMO_2,
    PESO_MAXIMO,
    RECARGO_FIN_SEMANA,
    TARIFA_TRAMO_1,
    TARIFA_TRAMO_2,
    UNO,
    VALOR_CENTENA,
)
from .estrategias_zona import EstrategiaZona, obtener_estrategia_zona


def validar_peso(peso: object) -> Decimal:
    """Convierte a Decimal y valida el intervalo abierto/cerrado de R1."""
    try:
        valor = Decimal(str(peso))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("peso debe ser un número válido") from exc

    if not valor.is_finite():
        raise ValueError("peso debe ser un número finito")
    if valor <= CERO:
        raise ValueError("peso debe ser mayor que 0")
    if valor > PESO_MAXIMO:
        raise ValueError(f"peso no puede superar {PESO_MAXIMO} kg")
    return valor


def validar_dia(dia: object) -> int:
    """Valida que el día sea un entero del 1 al 7."""
    if type(dia) is not int:
        raise ValueError("día debe ser un entero entre 1 y 7")
    if dia not in range(1, 8):
        raise ValueError("día debe ser un entero entre 1 y 7")
    return dia


def calcular_tarifa_base(peso: Decimal) -> Decimal:
    """Calcula los tres tramos, con L1 excluido del primer tramo."""
    if peso < LIMITE_TRAMO_1:
        return TARIFA_TRAMO_1
    if peso <= LIMITE_TRAMO_2:
        return TARIFA_TRAMO_2
    exceso = peso - LIMITE_TRAMO_2
    return TARIFA_TRAMO_2 + exceso * COSTO_POR_KG_ADICIONAL


def aplicar_descuento_cliente(subtotal: Decimal, cliente: str) -> Decimal:
    """Aplica el descuento conocido para frecuente o VIP; normal no descuenta."""
    descuentos = {
        "frecuente": DESCUENTO_FRECUENTE,
        "vip": DESCUENTO_VIP,
    }
    porcentaje = descuentos.get(cliente, CERO)
    return subtotal * (UNO - porcentaje)


def aplicar_cupon(subtotal: Decimal, cupon: str | None) -> Decimal:
    """Aplica ENVIO10; los códigos desconocidos se ignoran según R7."""
    if cupon == CODIGO_CUPON:
        return subtotal * (UNO - DESCUENTO_CUPON)
    return subtotal


def aplicar_costo_minimo(subtotal: Decimal) -> Decimal:
    """Aplica el piso monetario R8."""
    if subtotal < COSTO_MINIMO:
        return COSTO_MINIMO
    return subtotal


def redondear_a_centena(subtotal: Decimal) -> int:
    """Redondea al múltiplo de $100 más cercano, con empate hacia arriba."""
    centenas = (subtotal / VALOR_CENTENA).quantize(
        UNO, rounding=ROUND_HALF_UP
    )
    return int(centenas * VALOR_CENTENA)


class CalculadoraEnvios:
    """Contexto del patrón Estrategia: calcula con una zona inyectada."""

    def __init__(self, estrategia_zona: EstrategiaZona) -> None:
        self._estrategia_zona = estrategia_zona

    def calcular(
        self,
        peso: object,
        cliente: str,
        dia: object,
        cup: str | None = None,
    ) -> int:
        """Valida y aplica las reglas en el orden especificado."""
        peso_validado = validar_peso(peso)
        dia_validado = validar_dia(dia)

        if cup is not None and cup != "" and not self._estrategia_zona.permite_cupones:
            raise ValueError("la zona insular no admite cupones")

        subtotal = calcular_tarifa_base(peso_validado)
        subtotal = self._estrategia_zona.aplicar(subtotal)

        if dia_validado in DIAS_FIN_SEMANA:
            subtotal += RECARGO_FIN_SEMANA

        subtotal = aplicar_descuento_cliente(subtotal, cliente)
        subtotal = aplicar_cupon(subtotal, cup)
        subtotal = aplicar_costo_minimo(subtotal)
        return redondear_a_centena(subtotal)


def calc(
    peso: object,
    zona: str,
    cliente: str,
    dia: object,
    cup: str | None = None,
) -> int:
    """Selecciona una estrategia y delega el cálculo en el contexto."""
    estrategia_zona = obtener_estrategia_zona(zona)
    contexto = CalculadoraEnvios(estrategia_zona)
    return contexto.calcular(peso, cliente, dia, cup)
