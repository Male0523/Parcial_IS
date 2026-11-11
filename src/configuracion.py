"""Constantes de dominio para los parámetros personalizados de EnvíaYa."""

from decimal import Decimal

PESO_MAXIMO = Decimal("50")
LIMITE_TRAMO_1 = Decimal("3")
LIMITE_TRAMO_2 = Decimal("10")

TARIFA_TRAMO_1 = Decimal("6000")
TARIFA_TRAMO_2 = Decimal("9000")
COSTO_POR_KG_ADICIONAL = Decimal("800")

RECARGO_RURAL = Decimal("0.20")
RECARGO_NACIONAL = Decimal("0.50")
RECARGO_INSULAR = Decimal("0.70")
RECARGO_FIN_SEMANA = Decimal("2000")

DESCUENTO_FRECUENTE = Decimal("0.05")
DESCUENTO_VIP = Decimal("0.15")
CODIGO_CUPON = "ENVIO10"
DESCUENTO_CUPON = Decimal("0.10")

COSTO_MINIMO = Decimal("5000")
VALOR_CENTENA = Decimal("100")
UNO = Decimal("1")
CERO = Decimal("0")
DIAS_FIN_SEMANA = frozenset({6, 7})
