# Parte 3. Diseño de pruebas de caja negra — EnvíaYa

**Línea base del diseño:** requisitos personalizados R1–R8; las diferencias del código legado se documentan por separado.  
**Estado histórico:** al cierre de la Fase 3 estos casos eran un diseño no automatizado; posteriormente BB-01–BB-41 se automatizaron contra `src.calculadora.calc` y se ejecutaron en Actions. Las salidas esperadas siguen derivándose de R1–R8.

## 1. Parámetros y reglas aplicadas

| Regla | Valor |
|---|---:|
| PMAX | 50 kg |
| L1 | 3 kg; tramo 1 exige p < 3 |
| L2 | 10 kg; tramo 2 incluye 10 |
| Tarifa base | $6.000 / $9.000 |
| Exceso mayor a 10 kg | $800 por kg, proporcional |
| Recargos rural / nacional | 20 % / 50 % |
| Descuentos frecuente / VIP / ENVIO10 | 5 % / 15 % / 10 % |
| Fin de semana | $2.000 en días 6 y 7, antes de descuentos |
| Costo mínimo | $5.000 |
| Redondeo | Centena más cercana; empate de $50 hacia arriba |

Los descuentos se aplican secuencialmente: cliente y luego cupón. El piso y el redondeo se aplican al final. Importes en pesos colombianos.

## 2. Particiones de equivalencia

### Peso

| ID | Clase | Ejemplos/intervalo | Resultado requerido |
|---|---|---|---|
| P-V1 | Positivo menor que 3 | 0 < p < 3 | Tarifa base $6.000 |
| P-V2 | Desde 3 hasta 10 inclusive | 3 ≤ p ≤ 10 | Tarifa base $9.000 |
| P-V3 | Mayor que 10 y hasta 50 | 10 < p ≤ 50 | $9.000 + $800 × (p − 10) |
| P-I1 | Cero o negativo | p ≤ 0 | `ValueError` |
| P-I2 | Sobre PMAX | p > 50 | `ValueError` |
| P-A1 | No numérico | Ej. texto | Tipo no definido por el enunciado; no se fija expectativa adicional. |

### Zona

| ID | Valores | Clase y efecto |
|---|---|---|
| Z-V1 | urbana | Válida, 0 % |
| Z-V2 | rural | Válida, +20 % |
| Z-V3 | nacional | Válida, +50 % |
| Z-I1 | Otra zona | Inválida por R2; debe lanzar un error, sin clase de excepción prescrita. |

### Cliente

| ID | Valores | Clase y efecto |
|---|---|---|
| C-V1 | normal | Categoría enumerada; no se aplica descuento |
| C-V2 | frecuente | Categoría enumerada; 5 % |
| C-V3 | VIP | Categoría enumerada; 15 % |
| C-A1 | Otro valor | Ambigüedad: el enunciado no define rechazo ni comportamiento. No se etiqueta como inválido ni se exige excepción. |

### Día

| ID | Valores | Clase y efecto |
|---|---|---|
| D-V1 | Entero 1–5 | Válido, sin recargo de fin de semana |
| D-V2 | Entero 6 | Válido, sábado, +$2.000 |
| D-V3 | Entero 7 | Válido, domingo, +$2.000 |
| D-I1 | Entero <1 o >7 | Inválido, lanza error (clase no definida) |
| D-I2 | No entero, ej. 1.5 | Inválido porque se exige entero; lanza error (clase no definida) |

### Cupón

| ID | Valor | Clase y efecto |
|---|---|---|
| U-V1 | Ausente (`None`) | Válido, sin descuento |
| U-V2 | `ENVIO10` | Válido, 10 % |
| U-V3 | Código desconocido | Válido, ignorado sin descuento ni error |
| U-A1 | Tipo distinto de texto | Tipo no definido; no se inventa regla de validación. |

## 3. Análisis de valores límite

Para valores inmediatos se usan decimales explícitos permitidos para peso. Salvo que se indique, datos comunes: zona urbana, normal, día 1, sin cupón.

| Variable/límite | Inferior/inmediatamente antes | Exacto | Superior/inmediatamente después | Salida prevista |
|---|---:|---:|---:|---|
| Peso inferior | 0 (inválido) | 0 | 0.001 | 0 → `ValueError`; 0.001 → $6.000 |
| L1 = 3 | 2.999 | 3 | 3.001 | $6.000; $9.000; $9.000 |
| L2 = 10 | 9.999 | 10 | 10.001 | $9.000; $9.000; $9.000 tras redondeo de $9.000.80 |
| PMAX = 50 | 49.999 | 50 | 50.001 | $41.000; $41.000; `ValueError` |
| Día mínimo | 0 | 1 | — | Error; válido sin recargo |
| Día máximo | — | 7 | 8 | Válido con +$2.000; error |

En 49.999 kg: base = 9.000 + (49.999 − 10) × 800 = 40.999.20, redondeada a $41.000. En 50 kg: base = 9.000 + 40 × 800 = $41.000. En 10.001 kg el exceso vale $0.80, cuyo resultado sigue redondeando a $9.000.

## 4. Tabla de decisión: cliente × cupón × calendario

Base común: peso 3 kg, zona urbana, tarifa $9.000. Laboral es día 1–5; fin de semana es día 6 o 7. Cupón desconocido se ignora, por lo que su importe coincide con “sin cupón”.

| Cliente | Cupón | Laboral | Fin de semana (recargo primero) |
|---|---|---:|---:|
| Normal | Sin cupón | 9.000 → **$9.000** | (9.000+2.000) → **$11.000** |
| Normal | Desconocido | Ignorado → **$9.000** | 11.000; ignorado → **$11.000** |
| Normal | ENVIO10 | 9.000×0.90 = **$8.100** | 11.000×0.90 = **$9.900** |
| Frecuente | Sin cupón | 9.000×0.95=8.550 → **$8.600** | 11.000×0.95=10.450 → **$10.500** |
| Frecuente | Desconocido | Ignorado → **$8.600** | Ignorado → **$10.500** |
| Frecuente | ENVIO10 | 9.000×.95×.90=7.695 → **$7.700** | 11.000×.95×.90=9.405 → **$9.400** |
| VIP | Sin cupón | 9.000×.85=7.650 → **$7.700** | 11.000×.85=9.350 → **$9.400** |
| VIP | Desconocido | Ignorado → **$7.700** | Ignorado → **$9.400** |
| VIP | ENVIO10 | 9.000×.85×.90=6.885 → **$6.900** | 11.000×.85×.90=8.415 → **$8.400** |

## 5. Casos de prueba diseñados

Los datos se expresan como `(p, z, c, d, cup)`. Los casos de error esperan una excepción, sin exigir clase salvo R1. Los importes esperados están calculados conforme a la especificación. “EP” = particiones equivalentes; “BVA” = valores límite; “TD” = tabla de decisión. La columna “Resultado esperado” corresponde a los requisitos; no describe una ejecución del código heredado. Las diferencias estáticas identificadas se enumeran en la sección 9.

| ID | Req. | Técnica | Entrada | Resultado esperado | Justificación |
|---|---|---|---|---|---|
| BB-01 | R1 | EP/BVA | (0, urbana, normal, 1, None) | `ValueError` | Límite inferior excluido. |
| BB-02 | R1,R3 | EP/BVA | (0.001, urbana, normal, 1, None) | $6.000 | Peso positivo en tramo 1. |
| BB-03 | R3 | BVA | (2.999, urbana, normal, 1, None) | $6.000 | Inmediatamente bajo L1. |
| BB-04 | R3 | BVA | (3, urbana, normal, 1, None) | $9.000 | L1 inicia tramo 2. |
| BB-05 | R3 | BVA | (3.001, urbana, normal, 1, None) | $9.000 | Inmediatamente sobre L1. |
| BB-06 | R3 | BVA | (9.999, urbana, normal, 1, None) | $9.000 | Bajo L2. |
| BB-07 | R3 | BVA | (10, urbana, normal, 1, None) | $9.000 | L2 incluido. |
| BB-08 | R3,R8 | BVA | (10.001, urbana, normal, 1, None) | $9.000 | 9.000+0.001×800=9.000.80; nearest hundred $9.000. |
| BB-09 | R3,R8 | BVA | (49.999, urbana, normal, 1, None) | $41.000 | Base 40.999.20, redondea a $41.000. |
| BB-10 | R1,R3 | BVA | (50, urbana, normal, 1, None) | $41.000 | PMAX válido; base 41.000. |
| BB-11 | R1 | BVA | (50.001, urbana, normal, 1, None) | `ValueError` | Sobre PMAX. |
| BB-12 | R2 | EP/BVA | (3, urbana, normal, 0, None) | Error | Día debajo del rango. |
| BB-13 | R2,R5 | EP/BVA | (3, urbana, normal, 1, None) | $9.000 | Día mínimo válido. |
| BB-14 | R2,R5 | EP/BVA | (3, urbana, normal, 7, None) | $11.000 | Día máximo válido, domingo. |
| BB-15 | R2 | EP/BVA | (3, urbana, normal, 8, None) | Error | Día sobre el rango. |
| BB-16 | R4 | EP | (3, urbana, normal, 1, None) | $9.000 | Urbana 0 %. |
| BB-17 | R4 | EP | (3, rural, normal, 1, None) | $10.800 | 9.000×1.20. |
| BB-18 | R4 | EP | (3, nacional, normal, 1, None) | $13.500 | 9.000×1.50. |
| BB-19 | R2 | EP | (3, costera, normal, 1, None) | Error | Zona no admitida. |
| BB-20 | R2 | EP | (3, urbana, normal, 1.5, None) | Error | Día no entero. |
| BB-21 | R5 | BVA | (3, urbana, normal, 6, None) | $11.000 | Sábado también recibe $2.000. |
| BB-22 | R6 | TD | (3, urbana, normal, 1, None) | $9.000 | Normal, sin cupón, laboral. |
| BB-23 | R6,R7 | TD | (3, urbana, normal, 1, X) | $9.000 | Cupón inexistente ignorado. |
| BB-24 | R6 | TD | (3, urbana, normal, 1, ENVIO10) | $8.100 | Cupón válido, laboral. |
| BB-25 | R5,R6 | TD | (3, urbana, normal, 6, None) | $11.000 | Normal, sin cupón, fin de semana. |
| BB-26 | R5,R7 | TD | (3, urbana, normal, 6, X) | $11.000 | Cupón ignorado, fin de semana. |
| BB-27 | R5,R6 | TD | (3, urbana, normal, 6, ENVIO10) | $9.900 | 11.000×0.90. |
| BB-28 | R6,R8 | TD | (3, urbana, frecuente, 1, None) | $8.600 | 9.000×.95=8.550; empate sube. |
| BB-29 | R6,R7,R8 | TD | (3, urbana, frecuente, 1, X) | $8.600 | Cupón ignorado; descuento frecuente. |
| BB-30 | R6,R8 | TD | (3, urbana, frecuente, 1, ENVIO10) | $7.700 | 8.550×.90=7.695 → 7.700. |
| BB-31 | R5,R6,R8 | TD | (3, urbana, frecuente, 6, None) | $10.500 | 11.000×.95=10.450; empate sube. |
| BB-32 | R5,R6,R7,R8 | TD | (3, urbana, frecuente, 6, X) | $10.500 | Cupón ignorado; mismo resultado que sin cupón. |
| BB-33 | R5,R6,R8 | TD | (3, urbana, frecuente, 6, ENVIO10) | $9.400 | 11.000×.95×.90=9.405 → 9.400. |
| BB-34 | R6,R8 | TD | (3, urbana, vip, 1, None) | $7.700 | 9.000×.85=7.650; empate sube. |
| BB-35 | R6,R7,R8 | TD | (3, urbana, vip, 1, X) | $7.700 | Cupón ignorado. |
| BB-36 | R6,R8 | TD | (3, urbana, vip, 1, ENVIO10) | $6.900 | 9.000×.85×.90=6.885 → 6.900. |
| BB-37 | R5,R6,R8 | TD | (3, urbana, vip, 6, None) | $9.400 | 11.000×.85=9.350; empate sube. |
| BB-38 | R5,R6,R7,R8 | TD | (3, urbana, vip, 6, X) | $9.400 | Cupón ignorado. |
| BB-39 | R5,R6,R8 | TD | (3, urbana, vip, 6, ENVIO10) | $8.400 | 11.000×.85×.90=8.415 → 8.400. |
| BB-40 | R8 | BVA | (10.0625, urbana, normal, 1, None) | **Esperado R8: $9.100. Legado (deducción estática): $9.000 por truncamiento.** | Base 9.000+50=9.050; empate sube según requisito. El legado usa `int(t/100)*100` y trunca. |
| BB-41 | R8 | EP/cálculo | (0.001, urbana, vip, 1, ENVIO10) | $5.000 | 6.000×.85×.90=4.590; aplica costo mínimo. |

Los 18 casos BB-22–BB-39 recorren las 3 categorías de cliente × 3 clases de cupón × 2 calendarios. BB-23/26/29/32/35/38 usan el cupón desconocido; X representa cualquier código no reconocido.

## 6. Cálculos manuales paso a paso

### BB-03: inmediatamente debajo de 3 kg

2.999 está en 0 < p < 3; base $6.000. Urbana no recarga; día 1 no recarga; cliente normal y sin cupón no descuentan. Es mayor que el piso y múltiplo de $100. **Total: $6.000.**

### BB-04: exactamente 3 kg

La primera tarifa exige p < 3, por lo que no aplica. 3 ≤ p ≤ 10: base $9.000. No hay recargos ni descuentos; el piso no interviene. **Total: $9.000.**

### BB-08: apenas superior a 10 kg

Exceso = 10.001−10 = 0.001 kg. Cargo adicional = 0.001×$800 = $0.80. Base $9.000.80; está a $0.80 de $9.000 y $99.20 de $9.100. **Total: $9.000.**

### BB-33: fin de semana y ambos descuentos secuenciales

Base $9.000. Día 6 agrega $2.000 antes de descuentos: $11.000. Frecuente: $11.000×0.95=$10.450. Luego cupón: $10.450×0.90=$9.405. A $9.400 le separan $5 y a $9.500 le separan $95. **Total: $9.400.**

### BB-36: VIP y ENVIO10

Base $9.000. VIP primero: $9.000×0.85=$7.650. Cupón después: $7.650×0.90=$6.885. Se redondea a $6.900 (distancias $15 y $85). **Total: $6.900.**

### BB-40: empate exacto de $50

Exceso = 10.0625−10=0.0625 kg. Adicional = 0.0625×$800=$50. Base $9.050, exactamente a mitad entre $9.000 y $9.100. Por empate hacia arriba, **total: $9.100**.

### BB-41: costo mínimo

Base $6.000 (0.001 kg). Descuento VIP: $6.000×0.85=$5.100. ENVIO10: $5.100×0.90=$4.590. El costo calculado es menor a $5.000; aplica el piso. **Total: $5.000.**

## 7. Trazabilidad de requisitos

| Requisito | Casos de caja negra |
|---|---|
| R1 | BB-01, BB-02, BB-10, BB-11 |
| R2 | BB-12 a BB-15, BB-19, BB-20 |
| R3 | BB-02 a BB-10, BB-40 |
| R4 | BB-16 a BB-18 |
| R5 | BB-14, BB-21, BB-25 a BB-27, BB-31 a BB-33, BB-37 a BB-39 |
| R6 | BB-22 a BB-39 |
| R7 | BB-23, BB-26, BB-29, BB-32, BB-35, BB-38 |
| R8 | BB-08 a BB-10, BB-28, BB-30 a BB-41 |

## 8. Revisión del diseño

Hay 41 casos identificados, sin filas duplicadas. La matriz cubre límites indicados, las 18 combinaciones de la tabla de decisión, zonas, reglas de cupón, piso y redondeo. No se fija comportamiento para tipos de cliente, peso o cupón que el enunciado no especifica. No se han ejecutado pruebas ni se reportan métricas de ejecución.


## 9. Resultado requerido y comportamiento deducible del código heredado

Esta comparación es una **deducción por inspección estática** de `envios.py`, no una ejecución ni evidencia de prueba. “Esperado” aplica R1–R8; “legado” describe lo que el flujo actual devolvería o la excepción que produciría para la entrada indicada. Los casos no incluidos en la tabla no tienen una diferencia conocida al contrastar sus entradas y operaciones con la implementación.

| Caso | Resultado esperado por requisito | Comportamiento legado deducible estáticamente | Causa |
|---|---|---|---|
| BB-04 | $9.000 | $6.000 | La condición heredada usa `p <= L1`, por lo que incluye 3 kg en el tramo 1. |
| BB-09 | $41.000 | $40.900 | El importe previo es $40.999,20; `int(t/100)*100` trunca. |
| BB-12 | Error por día 0 | Retornaría $9.000 | No hay validación explícita del rango del día. |
| BB-15 | Error por día 8 | Retornaría $11.000 | No valida rango; `d > 6` agrega el recargo. |
| BB-19 | Error por zona no admitida | Retornaría $9.000 | Ninguna rama de zona coincide y el flujo continúa sin recargo ni error. |
| BB-20 | Error por día no entero | Retornaría $9.000 | No hay validación explícita de tipo/rango; 1.5 no satisface `d > 6`. |
| BB-21 | $11.000 | $9.000 | `d > 6` no incluye sábado (6). |
| BB-28, BB-29 | $8.600 | $8.500 | $8.550 se trunca a la centena inferior. |
| BB-30 | $7.700 | $7.600 | $7.695 se trunca a la centena inferior. |
| BB-31, BB-32 | $10.500 | $10.400 | $10.450, empate que R8 redondea hacia arriba, se trunca. |
| BB-34, BB-35 | $7.700 | $7.600 | $7.650, empate que R8 redondea hacia arriba, se trunca. |
| BB-36 | $6.900 | $6.800 | $6.885 se trunca a la centena inferior. |
| BB-37, BB-38 | $9.400 | $9.300 | $9.350, empate que R8 redondea hacia arriba, se trunca. |
| BB-40 | $9.100 | $9.000 | $9.050 es empate; el requisito sube y el legado trunca. |

En BB-33 ($9.405 → $9.400) y BB-39 ($8.415 → $8.400), la truncación heredada coincide por casualidad con el redondeo requerido. También coincide para casos como BB-08 ($9.000,80 → $9.000). Coincidencia del resultado en esos datos no significa que la estrategia heredada implemente redondeo al más cercano.
