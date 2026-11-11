# Fase 4. Resultados de automatización y pruebas — EnvíaYa

## 1. Alcance y línea base

Ejecución contra `envios.py` heredado, sin cambios funcionales. La suite automatiza los 41 casos BB-01 a BB-41 y los 15 recorridos P01 a P15. Las expectativas BB se mantienen derivadas de R1–R8; las aserciones P caracterizan el flujo legado para verificar caminos, no declaran válidos los resultados que incumplen requisitos. P01 usa `costera` solo como entrada estructural inválida por R2.

**Revisión de un oráculo de caja blanca:** en la primera ejecución P15 esperaba retorno 9.000 según la fila original de `docs/04_caja_blanca.md`, pero el legado devolvió 6.000 con p=3 por la condición `p <= L1`. Se actualizó la caracterización de P15 a 6.000 y se volvió a ejecutar. La expectativa funcional de BB-04 sigue siendo 9.000 por R3; esa discrepancia permanece como fallo y no se corrigió `envios.py`.

## 2. Ejecución final

- **Evidencia:** [GitHub Actions, ejecución 43107058958](https://github.com/Male0523/Parcial_IS/actions/runs/43107058958), commit `cefd3cff`, rama `docs/fase-2-plan-pruebas`.
- **Entorno:** GitHub Actions, Ubuntu 24.04.5, Python 3.12.16.
- **Instalación:** `python -m pip install -r requirements.txt` — paso completado.
- **Comando de prueba:** `python -m pytest -q tests/ --junitxml=evidencias/junit.xml --cov=envios --cov-branch --cov-report=term-missing --cov-report=json:evidencias/coverage.json`
- **Resultado:** 56 pruebas ejecutadas; **25 aprobadas, 31 fallidas, 0 errores técnicos**. Tiempo informado por pytest: 0,35 s.
- El job de Actions termina con estado fallido porque la suite conserva aserciones funcionales de R1–R8 y encontró discrepancias reales del legado. La instalación, descubrimiento y ejecución de pruebas sí finalizaron; no son fallos de entorno.

## 3. Resultados por caso fallido

Los importes de “Observado” y los retornos ante entradas R2 inválidas proceden de la salida real de pytest en la ejecución indicada.

| ID | Req. | Entrada (p, zona, cliente, día, cupón) | Esperado por requisito | Observado en legado | Defecto relacionado |
|---|---|---|---:|---:|---|
| BB-04 | R3 | (3, urbana, normal, 1, —) | $9.000 | $6.000 | DEF-01 |
| BB-09 | R3, R8 | (49.999, urbana, normal, 1, —) | $41.000 | $40.900 | DEF-04 |
| BB-12 | R2 | (3, urbana, normal, 0, —) | Error | Retornó $6.000 | DEF-02 |
| BB-13 | R2, R3 | (3, urbana, normal, 1, —) | $9.000 | $6.000 | DEF-01 |
| BB-14 | R3, R5 | (3, urbana, normal, 7, —) | $11.000 | $8.000 | DEF-01 |
| BB-15 | R2 | (3, urbana, normal, 8, —) | Error | Retornó $8.000 | DEF-02 |
| BB-16 | R3, R4 | (3, urbana, normal, 1, —) | $9.000 | $6.000 | DEF-01 |
| BB-17 | R3, R4 | (3, rural, normal, 1, —) | $10.800 | $7.200 | DEF-01 |
| BB-18 | R3, R4 | (3, nacional, normal, 1, —) | $13.500 | $9.000 | DEF-01 |
| BB-19 | R2 | (3, costera, normal, 1, —) | Error | Retornó $6.000 | DEF-02 |
| BB-20 | R2 | (3, urbana, normal, 1.5, —) | Error | Retornó $6.000 | DEF-02 |
| BB-21 | R3, R5 | (3, urbana, normal, 6, —) | $11.000 | $6.000 | DEF-01, DEF-03 |
| BB-22 | R3, R6 | (3, urbana, normal, 1, —) | $9.000 | $6.000 | DEF-01 |
| BB-23 | R3, R6, R7 | (3, urbana, normal, 1, X) | $9.000 | $6.000 | DEF-01 |
| BB-24 | R3, R6 | (3, urbana, normal, 1, ENVIO10) | $8.100 | $5.400 | DEF-01 |
| BB-25 | R3, R5 | (3, urbana, normal, 6, —) | $11.000 | $6.000 | DEF-01, DEF-03 |
| BB-26 | R3, R5, R7 | (3, urbana, normal, 6, X) | $11.000 | $6.000 | DEF-01, DEF-03 |
| BB-27 | R3, R5, R6 | (3, urbana, normal, 6, ENVIO10) | $9.900 | $5.400 | DEF-01, DEF-03 |
| BB-28 | R3, R6, R8 | (3, urbana, frecuente, 1, —) | $8.600 | $5.700 | DEF-01 |
| BB-29 | R3, R6, R7, R8 | (3, urbana, frecuente, 1, X) | $8.600 | $5.700 | DEF-01 |
| BB-30 | R3, R6, R8 | (3, urbana, frecuente, 1, ENVIO10) | $7.700 | $5.100 | DEF-01, DEF-04 |
| BB-31 | R3, R5, R6, R8 | (3, urbana, frecuente, 6, —) | $10.500 | $5.700 | DEF-01, DEF-03 |
| BB-32 | R3, R5, R6, R7, R8 | (3, urbana, frecuente, 6, X) | $10.500 | $5.700 | DEF-01, DEF-03 |
| BB-33 | R3, R5, R6, R8 | (3, urbana, frecuente, 6, ENVIO10) | $9.400 | $5.100 | DEF-01, DEF-03, DEF-04 |
| BB-34 | R3, R6, R8 | (3, urbana, vip, 1, —) | $7.700 | $5.100 | DEF-01 |
| BB-35 | R3, R6, R7, R8 | (3, urbana, vip, 1, X) | $7.700 | $5.100 | DEF-01 |
| BB-36 | R3, R6, R8 | (3, urbana, vip, 1, ENVIO10) | $6.900 | $5.000 | DEF-01, DEF-04 |
| BB-37 | R3, R5, R6, R8 | (3, urbana, vip, 6, —) | $9.400 | $5.100 | DEF-01, DEF-03 |
| BB-38 | R3, R5, R6, R7, R8 | (3, urbana, vip, 6, X) | $9.400 | $5.100 | DEF-01, DEF-03 |
| BB-39 | R3, R5, R6, R8 | (3, urbana, vip, 6, ENVIO10) | $8.400 | $5.000 | DEF-01, DEF-03, DEF-04 |
| BB-40 | R3, R8 | (10.0625, urbana, normal, 1, —) | $9.100 | $9.000 | DEF-04 |

Los 25 casos BB que usan peso exactamente 3 muestran primero la discrepancia de tarifa base de DEF-01; sus importes posteriores también reflejan las operaciones de zona, calendario y descuentos del legado. Los IDs que muestran varias causas están vinculados a todos los defectos pertinentes, no se cuentan como fallos adicionales por defecto.

## 4. Defectos confirmados

### DEF-01 — El límite de 3 kg se asigna a la tarifa inferior

- **Requisito:** R3.
- **Evidencia principal:** BB-04 usa p=3 kg; esperado $9.000 y observado $6.000. También se repite en BB-13–BB-14, BB-16–BB-18 y BB-21–BB-39.
- **Causa:** `envios.py` comprueba `p <= CONFIG["L1"]`; con L1=3 acepta el límite en el tramo de $6.000. R3 personalizado requiere p < 3.
- **Severidad:** Alta; afecta la tarifa base exactamente en el umbral y contamina los totales de varios recargos/descuentos.

### DEF-02 — No se rechazan zona y día inválidos

- **Requisito:** R2.
- **Evidencia:** BB-12, BB-15, BB-19 y BB-20 esperaban error; pytest observó retornos de $6.000, $8.000, $6.000 y $6.000, respectivamente.
- **Causa:** la función no valida explícitamente el rango/tipo del día ni el conjunto de zonas antes de calcular.
- **Severidad:** Media; se aceptan entradas que R2 manda rechazar, entregando cotizaciones aparentemente válidas.

### DEF-03 — El sábado no activa el recargo de fin de semana

- **Requisito:** R5.
- **Evidencia:** BB-14 (día 7) y BB-21 (día 6) usan los mismos demás datos: el legado devuelve $8.000 el domingo y $6.000 el sábado. La diferencia observada de $2.000 confirma que el recargo se aplica al día 7, pero no al 6; ambos deben tener el mismo recargo.
- **Causa:** la condición heredada es `d > 6`, que excluye sábado.
- **Severidad:** Media; los envíos sabatinos quedan sin el recargo definido de $2.000. Los importes también contienen el defecto de tarifa de BB-04.

### DEF-04 — El resultado trunca en vez de redondear a la centena más cercana

- **Requisito:** R8.
- **Evidencia:** BB-09: $40.999,20 debe redondear a $41.000, pero se observaron $40.900. BB-40: $9.050 debe subir a $9.100, pero se observaron $9.000.
- **Causa:** `int(t / 100) * 100` descarta la fracción en vez de aplicar redondeo al múltiplo más cercano con empate hacia arriba.
- **Severidad:** Media; produce importes inferiores al requerido, de forma sistemática para muchos valores que no son centenas exactas.

## 5. Otros hallazgos y límites de interpretación

- Los fallos de BB-17, BB-18, BB-24 y BB-27–BB-39 no demuestran por sí solos errores adicionales en las fórmulas de recargo/descuento: los casos usan p=3, cuya tarifa base heredada ya incumple R3. La comparación y el defecto quedan atribuidos a DEF-01, con DEF-03/DEF-04 cuando también intervienen.
- BB-41 pasó: el legado aplicó el piso de $5.000 en ese caso.
- BB-01–BB-03, BB-05–BB-08, BB-10–BB-11 y otros casos no incluidos en la tabla de fallos pasaron según las expectativas parametrizadas.
- La respuesta para valores de cliente no enumerados sigue siendo ambigua y no fue convertida en requisito de validación.
- La etapa P15 pasó tras alinear su oráculo estructural con el comportamiento observado; la expectativa funcional R3 sigue probándose separadamente con BB-04.

## 6. Cobertura real y relación con caminos

Salida de pytest-cov para `envios.py`:

| Medición | Resultado |
|---|---:|
| Sentencias | 29 de 29 ejecutadas; 0 sin cubrir; **100 %** |
| Ramas registradas por Coverage.py | 26 de 26 cubiertas; 0 parciales; **100 %** |
| Líneas no cubiertas | Ninguna |
| Ramas/decisiones no recorridas | Ninguna según Coverage.py |

P01–P15 se ejecutaron como caracterizaciones estructurales; en conjunto recorren rutas de validación, tramos, zonas, calendario, descuentos, cupón, piso, flag e impresión. Los 41 casos de caja negra también contribuyen a la cobertura. Coverage.py informa 26 aristas de rama a nivel de líneas; esto no equivale directamente a contar dos aristas por cada uno de los 14 predicados del grafo de `docs/04_caja_blanca.md`, pues la herramienta atribuye el cortocircuito de `p <= 0 or p > 50` a la línea condicional. Las entradas P02 (primer operando verdadero), P03 (primer falso, segundo verdadero) y entradas válidas ejercitan las alternativas de peso. Los porcentajes son resultados reales del comando indicado, no la estimación de diseño de la Parte 3.

## 7. Evidencias y comandos

El job publicó el artefacto **`enviaya-test-evidence-43107058958`** en la página de la [ejecución de GitHub Actions](https://github.com/Male0523/Parcial_IS/actions/runs/43107058958), con retención hasta el 9 de febrero de 2027. Contiene la salida de pytest/cobertura, XML JUnit, JSON de cobertura, código de salida y resumen. El log del job también conserva la salida completa.

Comandos ejecutados por el runner:

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests/ \
  --junitxml=evidencias/junit.xml \
  --cov=envios --cov-branch \
  --cov-report=term-missing \
  --cov-report=json:evidencias/coverage.json
```

Para repetir en Codespaces desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests/ --junitxml=evidencias/junit.xml --cov=envios --cov-branch --cov-report=term-missing --cov-report=json:evidencias/coverage.json
```

El resultado esperado de una repetición contra el mismo legado es que pytest termine con código 1 por las discrepancias funcionales documentadas; no se deben cambiar las expectativas para hacer verde la suite.
