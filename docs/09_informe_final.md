# Informe final del proyecto EnvíaYa

## Portada

**Proyecto:** EnvíaYa - Sistema de cálculo de costos de envío  
**Asignatura:** Ingeniería de Software I  
**Repositorio:** [Male0523/Parcial_IS](https://github.com/Male0523/Parcial_IS)  
**Rama integrada:** main  
**Commit consolidado de Fase 7:** 2db2f81d56d95930c5f35f9f63981ee4cc17c52c

| Campo académico | Información |
|---|---|
| Estudiante | [Nombre del estudiante] |
| Código registrado en los requisitos | 0182410122 |
| Docente | [Completar] |
| Institución | [Completar] |
| Fecha de entrega | [Completar] |

## 1. Introducción

Este informe consolida el proceso de ingeniería realizado para EnvíaYa: especificación de requisitos, diseño de pruebas, automatización, evaluación del código heredado, refactorización, control de versiones e incorporación de la zona insular de San Andrés.

El trabajo separa dos implementaciones con propósitos distintos. El archivo histórico envios.py conserva el código original para permitir su auditoría y caracterizar sus caminos de control. La implementación activa se organiza en src/ y recibe las correcciones y la nueva estrategia insular. Los resultados de pruebas se reportan por fase, sin mezclar la línea base heredada con las ejecuciones de la solución refactorizada.

## 2. Objetivos

### Objetivo general

Documentar y verificar el ciclo de vida de EnvíaYa desde los requisitos personalizados hasta una implementación modular probada, manteniendo trazabilidad entre especificación, diseño, código, pruebas e historial de Git.

### Objetivos específicos

- Formalizar R1-R8 y las reglas derivadas de los parámetros estudiantiles.
- Diseñar pruebas de caja negra y caja blanca antes de la automatización.
- Medir el comportamiento heredado frente a los resultados exigidos y registrar los defectos observados.
- Refactorizar la calculadora con responsabilidades separadas y el patrón Strategy.
- Incorporar la zona insular sin alterar las reglas de las zonas existentes ni el archivo heredado.
- Mantener evidencia real de pruebas y cobertura en GitHub Actions.
- Conservar historial, ramas, integraciones, etiquetas y notas de versión verificables.

## 3. Descripción y alcance

EnvíaYa calcula un costo de envío a partir del peso, la zona, el tipo de cliente, el día de la semana y, cuando está permitido, un cupón. La calculadora valida las entradas, establece una tarifa base, aplica recargos y descuentos en el orden especificado y normaliza el importe final.

La línea base original incluyó las zonas urbana, rural y nacional. La solicitud de cambio CAMBIO=0 incorporó posteriormente la zona insular de San Andrés en la implementación activa. La ampliación vive en src/; no modifica envios.py.

El alcance académico comprende requisitos funcionales, diseño y automatización de pruebas, refactorización, análisis de mantenibilidad, control de configuración y el cambio insular. No se documentan interfaces gráficas, persistencia, despliegue de producción ni reglas comerciales adicionales que no estén en el repositorio.

## 4. Parámetros personalizados

Los requisitos relacionan el código estudiantil 0182410122 con estos parámetros:

| Símbolo | Valor | Aplicación |
|---|---:|---|
| PMAX | 50 kg | Límite superior válido de peso |
| L1 | 3 kg | Límite entre el primer y segundo tramo |
| L2 | 10 kg | Límite superior del segundo tramo |
| RR | 20 % | Recargo rural |
| RN | 50 % | Recargo nacional |
| V | 15 % | Descuento VIP |
| S | $2.000 | Recargo de sábado y domingo |
| CAMBIO | 0 | Solicitud de incorporar San Andrés, zona insular |

También se aplican tarifa frecuente de 5 %, cupón ENVIO10 de 10 % y costo mínimo de $5.000. Las reglas de paridad registradas son: D=1 impar, por lo que el primer tramo exige peso menor que 3 kg; E=2 par, así que el recargo de fin de semana antecede a los descuentos; B=1 impar, por lo que los descuentos coincidentes se aplican primero al cliente y después al cupón; F=2 par, por lo que cupones desconocidos se ignoran en las zonas que los admiten.

## 5. Requisitos funcionales R1-R8

La línea base se encuentra en [docs/01_requisitos.md](01_requisitos.md). La solicitud de la zona insular se registra aparte; no se renumeraron los requisitos originales.

| Requisito | Regla consolidada |
|---|---|
| R1 - Peso | Se admite 0 < peso <= 50 kg, incluidos decimales. La infracción produce ValueError. |
| R2 - Zona y día | La línea base admite urbana, rural o nacional; el día debe ser entero de 1 a 7. Entradas fuera del dominio deben generar un error, sin que el requisito base fije una clase específica para zona o día. |
| R3 - Tarifa base | Menos de 3 kg: $6.000. Desde 3 hasta 10 kg inclusive: $9.000. Sobre 10 kg: $9.000 más $800 por kilogramo proporcional de exceso. |
| R4 - Zona | Urbana: 0 %. Rural: 20 %. Nacional: 50 %. La zona insular se agrega después mediante CAMBIO=0. |
| R5 - Fin de semana | Días 6 y 7 agregan $2.000 antes de descuentos. |
| R6 - Descuentos | Frecuente: 5 %. VIP: 15 %. ENVIO10: 10 %. Si coinciden cliente y cupón, primero se aplica cliente y luego cupón. |
| R7 - Cupón desconocido | Se ignora sin descuento ni error en las zonas que aceptan cupones. La solicitud insular establece una excepción por zona. |
| R8 - Mínimo y redondeo | El costo no baja de $5.000. Se redondea al múltiplo de $100 más cercano; los empates de $50 suben. |

La especificación no convierte el tipo de cliente desconocido en una validación obligatoria; esa ambigüedad permanece documentada en los requisitos.

## 6. Auditoría del código heredado

El artefacto heredado se agregó en el commit 8fdc6625efaffb39dcb70d57c9495503fc096306. El blob de envios.py en main conserva el SHA 5585b110170a271dadc20c11d67f8c62fb9a0b3c, igual al del contenido original. La función heredada calc(p, z, c, d, cup=None, flag=False) no fue modificada; las pruebas P01-P15 continúan apuntando a ella.

La Fase 4 confirmó cuatro defectos frente a R1-R8:

| Defecto | Evidencia de línea base | Requisito |
|---|---|---|
| DEF-01 - Límite de 3 kg asignado al tramo inferior | BB-04 esperaba $9.000 y observó $6.000 por la condición heredada p <= L1. | R3 |
| DEF-02 - Zona y día inválidos aceptados | BB-12, BB-15, BB-19 y BB-20 esperaban error; el legado retornó un importe. | R2 |
| DEF-03 - Sábado sin recargo | El código probaba d > 6, por lo que el día 6 no recibía $2.000. | R5 |
| DEF-04 - Truncamiento monetario | BB-40 requería $9.100 desde $9.050 y observó $9.000; BB-09 requería $41.000 y observó $40.900. | R8 |

Estos hallazgos son distintos de los malos olores de diseño. El informe de Fase 5 identifica, entre otros, Long Method, Magic Numbers, argumento flag, efecto de consola dentro del cálculo, asignación redundante, condicionales de zona y comparación no idiomática con None.

## 7. Diseño de pruebas

### 7.1 Caja negra

La matriz de [docs/03_caja_negra.md](03_caja_negra.md) diseña 41 casos BB-01 a BB-41 mediante:

- Particiones de equivalencia para peso, zona, cliente, día y cupón, distinguiendo entradas válidas e inválidas sin inventar restricciones no especificadas.
- Análisis de valores límite en peso: 0, inmediatamente sobre 0, a ambos lados de 3, exactamente 3, a ambos lados de 10, exactamente 10, debajo y en PMAX, y sobre PMAX. También considera los días 0, 1, 7 y 8.
- Tabla de decisión para cliente normal, frecuente y VIP; cupón ausente, desconocido o ENVIO10; día laboral o de fin de semana. Son 3 x 3 x 2, es decir 18 combinaciones. El fin de semana se suma antes de descuentos y el descuento de cliente precede al cupón.

Los resultados esperados de caja negra representan requisitos; la documentación separa esos resultados del comportamiento legado deducido u observado.

### 7.2 Caja blanca

[docs/04_caja_blanca.md](04_caja_blanca.md) contiene el grafo Mermaid, 30 nodos, 43 aristas, un componente conectado y 14 nodos predicado para calc heredada. La complejidad ciclomática es 15 por los tres métodos:

- Aristas, nodos y componentes: V(G) = 43 - 30 + 2(1) = 15.
- Predicados: 14 + 1 = 15.
- Regiones: 15.

Se documentan 15 caminos independientes P01-P15 y sus entradas. P01 usa costera solo para recorrer estructuralmente el camino del legado; costera es inválida según R2 y no es un caso funcional aceptado.

## 8. Automatización y resultados por etapa

La estructura automatizada está en tests/:

- test_caja_negra.py: 41 casos funcionales BB contra la calculadora activa tras la refactorización.
- test_caja_blanca.py: 15 caminos P contra envios.py heredado.
- test_regresion.py: siete comprobaciones defensivas adicionales.
- test_zona_insular.py: 12 ejecuciones nuevas parametrizadas para la solicitud insular y la paridad de cupones en otras zonas.

El workflow .github/workflows/tests.yml instala pytest y pytest-cov, ejecuta la suite y conserva JUnit XML, salida de pytest, JSON de cobertura y resumen como artefactos. Las cifras siguientes corresponden a etapas y objetos medidos distintos:

| Etapa y evidencia | Resultado de pruebas | Cobertura reportada |
|---|---|---|
| Fase 4, run 43107058958, código heredado | 56 ejecutadas: 25 aprobadas, 31 fallidas y 0 errores técnicos. Las fallas fueron discrepancias funcionales respecto de los requisitos. | envios.py: 29/29 sentencias y 26/26 ramas, 100 %. |
| Fase 5, run 43109179938, rama refactor/estrategia | 63 aprobadas, 0 fallidas y 0 errores. | src/: 99/99 sentencias y 20/20 ramas, 100 %. |
| Fase 7 RED, run 43114555953, antes de implementar zona insular | 75 ejecutadas: 64 aprobadas y 11 fallidas esperadas por zona aún no soportada. | src/: 99/99 sentencias y 20/20 ramas, 100 %. |
| Fase 7 GREEN, run 43114870307 | 75 aprobadas, 0 fallidas y 0 errores. | src/: 110/110 sentencias y 22/22 ramas, 100 %. |
| Repetición documental, run 43115183647 | 75 aprobadas, 0 fallidas y 0 errores. | src/: 110/110 sentencias y 22/22 ramas, 100 %. |

Los runs RED y GREEN de Fase 7 ocurrieron en feature/zona-insular antes de su PR de integración. El PR #3 integró el cambio en main; no se atribuye una ejecución local ni un run de Actions en main. La repetición documental también fue una ejecución real de Actions, no una afirmación de ejecución local.

## 9. Refactorización y arquitectura

La implementación activa separa configuración y responsabilidades:

- src/configuracion.py define constantes con Decimal.
- src/estrategias_zona.py contiene el protocolo EstrategiaZona, las estrategias urbana, rural, nacional e insular, y el registro de selección.
- src/calculadora.py valida peso y día, calcula tarifas, coordina el contexto CalculadoraEnvios, aplica la política de cupón y delega recargos por zona.
- tests/ protege la conducta funcional activa y conserva la caracterización de envios.py.

El patrón Strategy evita mantener la fórmula de recargo de cada zona en un único condicional. La estrategia concreta modifica el subtotal; el contexto conserva orden común para fin de semana, descuentos, costo mínimo y redondeo.

La comparación cuantitativa documentada en Fase 5 usa la medición de esa fase, anterior a la estrategia insular:

| Métrica | Heredado | Refactorización medida en Fase 5 |
|---|---:|---:|
| Complejidad de calc | 15 | 1 |
| Complejidad del método de contexto | No existía | 2 |
| Mayor complejidad de función individual | calc: 15 | validar_peso: 5 |
| Líneas físicas en la medición documentada | envios.py: 40 | src/*.py: 208 |
| Cobertura | envios.py: 29 sentencias, 26 ramas | src/: 99 sentencias, 20 ramas |

La suma de complejidad por bloques nuevos fue 27; no se presenta como una reducción, ya que las responsabilidades extraídas crean más funciones. La cobertura posterior a Fase 7 es distinta: src/ mide 110 sentencias y 22 ramas. La mayor extensión de líneas refleja separación, documentación y estrategia, no un aumento comparable de complejidad por función.

## 10. Gestión de configuración

La auditoría previa de Fase 8 se realizó sobre las referencias remotas de GitHub. main apunta al commit 2db2f81d56d95930c5f35f9f63981ee4cc17c52c; los PR de integración están cerrados y fusionados. Esta sesión no tenía un checkout local del repositorio, por lo que no se afirma un resultado local de git status ni un estado de archivos sin commit:

| PR | Integración | Merge commit |
|---|---|---|
| #1 | Suite BB-01-BB-41 y P01-P15 | 24dd66794b604dfb938a6fba0759f14c1d74a1de |
| #2 | Refactorización y estrategia | af258871346022904ebdf8fac7bfb629464bcea3 |
| #3 | Zona insular, pruebas TDD y documentos v1.2.0 | 2db2f81d56d95930c5f35f9f63981ee4cc17c52c |

Se conservan las ramas docs/fase-2-plan-pruebas, test/suite, refactor/estrategia y feature/zona-insular, además de main. Los commits relevantes incluyen 8fdc662 (registro heredado), d796c2f (casos BB), d0e8a07 (caminos P), 857388d (implementación Strategy de Fase 5), d319927 (pruebas insulares previas al cambio), 56509e1 (estrategia insular) y 2db2f81 (integración de Fase 7).

La etiqueta anotada v1.0.0 apunta al commit heredado 8fdc6625efaffb39dcb70d57c9495503fc096306. El changelog y las notas documentan v1.0.0, v1.1.0 y v1.2.0; la auditoría de refs encontró únicamente la etiqueta v1.0.0. Por tanto, v1.1.0 y v1.2.0 se describen como versiones documentadas, no como etiquetas verificadas.

CHANGELOG.md sigue Keep a Changelog y diferencia adiciones, cambios, correcciones, calidad y compatibilidad. Las notas están en docs/releases/.

## 11. Incorporación de la zona insular

CAMBIO=0 solicita la zona insular de San Andrés con recargo de 70 %. La estrategia se incorporó en src/estrategias_zona.py y se selecciona como insular. El cambio conserva validaciones globales de peso y día, recargo de fin de semana antes de descuentos, descuentos frecuente y VIP, mínimo y redondeo.

En zona insular, None y la cadena vacía se tratan como ausencia de cupón. Cualquier cupón proporcionado, conocido o desconocido, se rechaza. En las demás zonas se mantiene R7/F=2 y los códigos desconocidos se ignoran.

El enunciado no prescribe tipo de excepción ni mensaje para el cupón prohibido. Se eligió ValueError con el mensaje documentado en Fase 7; es una decisión técnica coherente con la validación de entradas, no una exigencia textual. La solicitud es aditiva y se registra como v1.2.0.

La evidencia TDD es RED en run 43114555953 y GREEN en run 43114870307, seguida por run 43115183647 tras actualizar documentación. El informe del cambio contiene casos, resultados, decisiones y enlaces a los artefactos.

## 12. Conclusiones

La trazabilidad se conserva desde las reglas personalizadas y las historias HU-01 a HU-03 hasta los casos de caja negra, caminos de caja blanca, funciones y evidencia de Actions. La evaluación heredada hizo visibles cuatro defectos sin alterar el artefacto histórico. La refactorización separó validación, cálculo y estrategia; la zona insular se añadió como una estrategia compatible con el flujo existente.

La evidencia de cobertura al 100 % se presenta siempre asociada a su fase y objeto medido. En particular, el 100 % sobre envios.py de Fase 4 no significa que las reglas fueran funcionalmente correctas: la suite heredada tuvo 31 fallas legítimas frente a requisitos. Las 75 pruebas aprobadas y la cobertura 110/110 sentencias y 22/22 ramas pertenecen a las ejecuciones GREEN de la calculadora activa. No se reporta ejecución local ni de Actions sobre el commit final de main.

## 13. Matriz de trazabilidad

| Requisito o cambio | Definición | Casos | Implementación relacionada | Evidencia verificable |
|---|---|---|---|---|
| R1 - Peso | docs/01_requisitos.md | BB-01, BB-02, BB-10, BB-11; P02-P04 | src/calculadora.py: validar_peso | Fase 5 run 43109179938; suite GREEN run 43115183647 |
| R2 - Zona y día | docs/01_requisitos.md; expansión insular en docs/08_cambio_insular.md | BB-12-BB-15, BB-19-BB-20; P01-P03 | src/calculadora.py: validar_dia; src/estrategias_zona.py: obtener_estrategia_zona | Fase 4 run 43107058958; GREEN run 43115183647 |
| R3 - Tarifa base | docs/01_requisitos.md | BB-02-BB-10, BB-40; P04-P06 | src/calculadora.py: calcular_tarifa_base | Fase 4 run 43107058958; Fase 5 run 43109179938 |
| R4 - Recargo zonal | docs/01_requisitos.md; cambio insular en docs/08_cambio_insular.md | BB-16-BB-18; INS-01, INS-06-INS-09; P06-P08 | src/estrategias_zona.py; src/configuracion.py | GREEN runs 43114870307 y 43115183647 |
| R5 - Fin de semana | docs/01_requisitos.md | BB-14, BB-21, BB-25-BB-27, BB-31-BB-33, BB-37-BB-39; INS-08-INS-09; P09 | src/calculadora.py: CalculadoraEnvios.calcular | GREEN run 43115183647 |
| R6 - Descuentos | docs/01_requisitos.md | BB-22-BB-39; INS-06-INS-09; P10-P13 | src/calculadora.py: aplicar_descuento_cliente y aplicar_cupon | Fase 5 run 43109179938; GREEN run 43115183647 |
| R7 - Cupón desconocido | docs/01_requisitos.md; excepción por zona en docs/08_cambio_insular.md | BB-23, BB-26, BB-29, BB-32, BB-35, BB-38; INS-02-INS-05 e INS-12; P01, P12-P13 | src/calculadora.py: aplicar_cupon; política permite_cupones en src/estrategias_zona.py | RED run 43114555953; GREEN run 43115183647 |
| R8 - Mínimo y redondeo | docs/01_requisitos.md | BB-08-BB-10, BB-28, BB-30-BB-41; P14 | src/calculadora.py: aplicar_costo_minimo y redondear_a_centena | Fase 5 run 43109179938; GREEN run 43115183647 |
| Cambio CAMBIO=0 - Zona insular | docs/01_requisitos.md y docs/08_cambio_insular.md | INS-01-INS-11; INS-12 conserva R7 en urbana | src/configuracion.py: RECARGO_INSULAR; src/estrategias_zona.py: ZonaInsular | RED 43114555953; GREEN 43114870307; repetición 43115183647 |

## 14. Referencias internas y evidencias

- [Requisitos y criterios de aceptación](01_requisitos.md)
- [Plan de pruebas](02_plan_pruebas.md)
- [Diseño de caja negra](03_caja_negra.md)
- [Diseño de caja blanca](04_caja_blanca.md)
- [Resultados de pruebas de Fase 4 y anotación histórica posterior](05_resultados_pruebas.md)
- [Refactorización y comparación](06_refactorizacion.md)
- [Gestión de configuración](07_gestion_configuracion.md)
- [Cambio insular, TDD y resultados](08_cambio_insular.md)
- [Changelog](../CHANGELOG.md)
- Notas de versión: [1.0.0](releases/v1.0.0.md), [1.1.0](releases/v1.1.0.md), [1.2.0](releases/v1.2.0.md)
- GitHub Actions: [Fase 4, run 43107058958](https://github.com/Male0523/Parcial_IS/actions/runs/43107058958), [Fase 5, run 43109179938](https://github.com/Male0523/Parcial_IS/actions/runs/43109179938), [Fase 7 RED, run 43114555953](https://github.com/Male0523/Parcial_IS/actions/runs/43114555953), [Fase 7 GREEN, run 43114870307](https://github.com/Male0523/Parcial_IS/actions/runs/43114870307), [repetición documental, run 43115183647](https://github.com/Male0523/Parcial_IS/actions/runs/43115183647).
- Integraciones: [PR #1](https://github.com/Male0523/Parcial_IS/pull/1), [PR #2](https://github.com/Male0523/Parcial_IS/pull/2), [PR #3](https://github.com/Male0523/Parcial_IS/pull/3).
