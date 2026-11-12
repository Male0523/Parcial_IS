# Fase 7. Incorporación de zona insular — San Andrés

## 1. Descripción

Se añadió la zona `insular` a la calculadora activa de EnvíaYa mediante el patrón Strategy. Aplica un recargo de 70% sobre la tarifa base y conserva el flujo compartido de fin de semana, descuentos, cupón (sujeto a la restricción propia de la zona), costo mínimo y redondeo. La zona no admite cupones suministrados; `None` y la cadena vacía significan que no se suministró cupón. Las demás zonas mantienen su política anterior: los cupones desconocidos se ignoran (R7, paridad F=2).

`envios.py` no fue modificado. La prueba P01 continúa apuntando al flujo heredado, mientras los casos funcionales nuevos ejercitan `src.calculadora.calc`.

## 2. Análisis de impacto

| Área | Impacto |
|---|---|
| Selección de zona | Se registra la clave `insular` en el selector existente; las demás claves conservan sus estrategias. |
| Estrategias | Se agrega una estrategia concreta con recargo 70% y propiedad de política de cupón. Las estrategias existentes declaran que sí permiten cupón. |
| Cálculo | El contexto común valida la política de cupones de la estrategia después de las validaciones generales de peso y día. Recargo de fin de semana y descuentos siguen en el mismo orden y código compartido. |
| Pruebas | Se agrega `tests/test_zona_insular.py` con 12 ejecuciones nuevas parametrizadas; se mantienen todas las pruebas existentes. |
| CI | Se incorpora `feature/zona-insular` a las ramas que ejecuta el workflow, para capturar RED y GREEN en Actions con artefactos verificables. |
| Documentación/versionamiento | Este informe, changelog y notas de v1.2.0. |

No se cambió la arquitectura general, los parámetros de otras zonas, los resultados esperados existentes ni la implementación histórica.

## 3. Requisitos y reglas afectadas

- **Nuevo requisito de zona insular:** recargo 70% para San Andrés.
- **Nuevo requisito de cupón por zona:** la zona insular rechaza cualquier cupón suministrado, incluso si no existe.
- **R1 y R2:** se reutilizan las validaciones globales existentes de peso y día.
- **R5:** el recargo de fin de semana de $2.000 sigue antes de los descuentos.
- **R6:** se conservan los descuentos frecuente (5%) y VIP (15%).
- **R7 / paridad F=2:** ENVIO10 sigue aplicándose en zonas que lo admiten; los cupones desconocidos de otras zonas siguen ignorándose.
- **R8:** se conserva el mínimo de $5.000 y el redondeo al centenar más cercano.

El costo mínimo es parte del pipeline compartido, aunque con los parámetros actuales de tarifa, zona insular y descuentos sin cupón, sus importes válidos no bajan de $5.000. La regresión existente BB-41 conserva una comprobación ejecutable del mínimo en la calculadora común.

## 4. Clases, funciones y archivos afectados

- `src/configuracion.py`: nueva constante `RECARGO_INSULAR = Decimal("0.70")`.
- `src/estrategias_zona.py`: el protocolo `EstrategiaZona` declara `permite_cupones`; urbana, rural y nacional lo mantienen en `True`; se agrega `ZonaInsular` con `permite_cupones = False` y su cálculo porcentual; se registra en `ESTRATEGIAS_ZONA`.
- `src/calculadora.py`: `CalculadoraEnvios.calcular` rechaza cupón no vacío cuando la estrategia no lo permite. Después delega en el mismo flujo de descuento/costo mínimo/redondeo.
- `tests/test_zona_insular.py`: pruebas de aceptación nuevas.
- `.github/workflows/tests.yml`: habilita la rama feature en CI.
- `CHANGELOG.md`, `docs/releases/v1.2.0.md` y este documento: registro del cambio.

No se implementó un tipo de cliente nuevo ni se agregó validación de cliente desconocido.

## 5. Casos nuevos y cálculos esperados

Los resultados se calcularon a mano con tarifa base $9.000 a 3 kg; no se derivan de la implementación probada.

| Caso | Escenario | Resultado esperado |
|---|---|---:|
| INS-01 | Normal, día laboral, cupón omitido | $15.300 |
| INS-02 | Cupón `None` | $15.300 |
| INS-03 | Cupón vacío `""` | $15.300 |
| INS-04 | Cupón `ENVIO10` suministrado | `ValueError` técnica |
| INS-05 | Cupón desconocido suministrado | `ValueError` técnica |
| INS-06 | Frecuente, día laboral | $14.500 |
| INS-07 | VIP, día laboral | $13.000 |
| INS-08 | VIP, domingo | $14.700 |
| INS-09 | Frecuente, sábado | $16.400 |
| INS-10 | Peso cero | `ValueError` de validación general de peso |
| INS-11 | Día 8 | `ValueError` de validación general de día |
| INS-12 | Urbana con cupón desconocido | $9.000; cupón ignorado por R7/F=2 |
| INS-13 | Rural, 11 kg, frecuente y ENVIO10, día laboral | $10.100 |
| INS-14 | Rural, 50 kg, VIP, sábado | $43.500 |
| INS-15 | Nacional, 11 kg, frecuente, día laboral | $14.000 |
| INS-16 | Nacional, 50 kg, ENVIO10, domingo | $57.200 |
| INS-17 | Insular, 11 kg, frecuente, día laboral | $15.800 |
| INS-18 | Insular, 50 kg, VIP, domingo | $60.900 |

**Cálculos representativos:**

1. INS-01: $9.000 × 1,70 = **$15.300**.
2. INS-06: $15.300 × 0,95 = $14.535 → **$14.500**.
3. INS-07: $15.300 × 0,85 = $13.005 → **$13.000**.
4. INS-08: ($9.000 × 1,70 + $2.000) × 0,85 = $14.705 → **$14.700**.
5. INS-09: ($9.000 × 1,70 + $2.000) × 0,95 = $16.435 → **$16.400**.

La batería completa conserva además BB-01–BB-41, P01–P15 y siete regresiones defensivas anteriores. INS-13–INS-18 amplían la comprobación de recargos rurales, nacionales e insulares sobre el tramo proporcional y PMAX, con descuentos y, donde se indica, fin de semana.

**Cálculos de INS-13–INS-18:**

- INS-13: base $9.800; rural $11.760; frecuente $11.172; ENVIO10 $10.054,80; redondeo → **$10.100**.
- INS-14: base $41.000; rural $49.200; sábado +$2.000 = $51.200; VIP $43.520; redondeo → **$43.500**.
- INS-15: base $9.800; nacional $14.700; frecuente $13.965; redondeo → **$14.000**.
- INS-16: base $41.000; nacional $61.500; domingo +$2.000 = $63.500; ENVIO10 $57.150; empate → **$57.200**.
- INS-17: base $9.800; insular $16.660; frecuente $15.827; redondeo → **$15.800**.
- INS-18: base $41.000; insular $69.700; domingo +$2.000 = $71.700; VIP $60.945; redondeo → **$60.900**.

## 6. Evidencia TDD: RED y GREEN

### RED — comportamiento antes de implementar

- Pruebas añadidas primero en commit `d3199270904c1a7d63fadbb4eba02a48f71d3872`.
- El workflow se habilitó para la rama feature en `9b8055d33b71158248157f134fda3a2667a8eafe`.
- GitHub Actions [run 43114555953](https://github.com/Male0523/Parcial_IS/actions/runs/43114555953), commit `9b8055d`: **75 ejecutadas, 64 aprobadas, 11 fallidas**. Las 11 fallas corresponden a las expectativas insulares aún no soportadas; la prueba INS-12 de cupón desconocido urbano ya pasó. El error observado fue `ValueError: zona no válida: 'insular'`; para entradas inválidas de peso/día el selector desconocido también impedía llegar a las validaciones generales. No fueron errores técnicos de entorno.
- El artefacto real `enviaya-test-evidence-43114555953` contiene JUnit, log y cobertura. La cobertura de `src/` fue 100% en esa ejecución RED, sin que eso signifique que la función requerida estuviera implementada.

### GREEN — comportamiento implementado

- Implementación en commit `56509e1cb031e79d7a9e4ee8a066963aeeb6c179`.
- GitHub Actions [run 43114870307](https://github.com/Male0523/Parcial_IS/actions/runs/43114870307), commit `56509e1`: **75 aprobadas, 0 fallidas, 0 errores**, 0,13 s.
- Cobertura de `src/`: **110/110 sentencias (100%) y 22/22 ramas (100%)**; el log muestra cero líneas y ramas no cubiertas.
- Artefacto real: `enviaya-test-evidence-43114870307` con JUnit XML, salida de pytest, JSON de cobertura y código de salida. Los artefactos de Actions tienen retención hasta el 9 de febrero de 2027.

## 7. Regresión

Las 63 pruebas preexistentes siguieron aprobadas:

- BB-01–BB-41 comprueban la conducta funcional de las zonas anteriores y los requisitos R1–R8.
- P01–P15 siguen caracterizando únicamente `envios.py` heredado.
- Siete casos defensivos continúan validando entradas no numéricas/no finitas, día booleano y zona de tipo inválido.
- INS-12 confirma explícitamente que los cupones desconocidos de una zona distinta de insular siguen ignorándose.
- Las pruebas originales que usan `ENVIO10` mantienen sus importes esperados.

No se alteraron expectativas para conseguir verde.

## 8. Tipo de mantenimiento

- **Adaptativo (principal):** el dominio incorpora San Andrés como una zona admitida con recargo y política de cupones propios.
- **Preventivo (complementario):** pruebas RED/GREEN, cobertura de ramas y ejecución del workflow en la rama feature ayudan a detectar regresiones futuras.
- No se clasifica como correctivo: no se reparó un defecto previo de las zonas ya existentes.

## 9. Decisiones y ambigüedades

La regla dice que la zona insular no admite cupones, pero no prescribe clase de excepción ni texto. Se eligió técnicamente `ValueError`, coherente con las otras entradas inválidas del cálculo, con mensaje `la zona insular no admite cupones`. Esto es una decisión de implementación; no se presenta como literal del requisito.

`None` y `""` se tratan como ausencia de cupón. Cualquier otro valor suministrado se rechaza en insular, incluso `ENVIO10` o un código desconocido. En urbana, rural y nacional se preserva R7: cupón desconocido se ignora. No se especificó una validación nueva para el tipo de objeto del cupón; la API mantiene el contrato existente `str | None`.

La incorporación es compatible y se registra como v1.2.0: agrega una clave y una estrategia, sin retirar ni cambiar la API actual. No se implementó la zona insular en `envios.py` heredado ni se avanzó a Fase 8.


## Verificación adicional en la rama correctiva

Después de ampliar los casos INS-13–INS-18 y corregir P12, GitHub Actions ejecutó el workflow completo en el commit `08dcbd9b2d81de87e86202e27a11447a67d4f563` (run [43133563143](https://github.com/Male0523/Parcial_IS/actions/runs/43133563143)). Las cuatro invocaciones configuradas aprobaron 81 pruebas; la medición de cobertura de `src/` fue 110/110 sentencias y 22/22 ramas (100 %). Esto es evidencia de la rama del PR #7, no una nueva ejecución de Fase 7 ni un resultado del HEAD de `main`. El artefacto `enviaya-test-evidence-43133563143` contiene los reportes de esa ejecución.
