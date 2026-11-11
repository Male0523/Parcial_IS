# Parte 3. Diseño de pruebas de caja negra — EnvíaYa

**Línea base:** requisitos personalizados de `docs/01_requisitos.md` y código original de `envios.py`.  
**Estado:** casos diseñados; todavía no automatizados ni ejecutados. Los resultados esperados de este documento se derivan de los requisitos, no de una ejecución del código.

## 1. Parámetros y reglas aplicados

| Regla | Valor aplicado |
|---|---:|
| PMAX | 50 kg |
| L1 | 3 kg; el primer tramo es estrictamente menor que 3 |
| L2 | 10 kg; el segundo tramo incluye 10 |
| Tarifa tramo 1 / tramo 2 | $6.000 / $9.000 |
| Exceso sobre 10 kg | $800 por kg proporcional |
| Recargo rural / nacional | 20 % / 50 % |
| Descuento frecuente / VIP | 5 % / 15 % |
| Cupón ENVIO10 | 10 % |
| Fin de semana | $2.000 para días 6 y 7, antes de descuentos |
| Mínimo | $5.000 |
| Redondeo | centena más cercana; empate de $50 hacia arriba |

Para casos con dos descuentos se calcula primero el porcentaje del cliente y luego el 10 % del cupón. Todo importe se normaliza al final: piso de $5.000 y redondeo indicado. Las cifras monetarias están en pesos colombianos.

## 2. Particiones de equivalencia

### 2.1 Peso

| Clase | Intervalo/ejemplos | Validez | Resultado especificado |
|---|---|---|---|
| P-V1 | 0 < p < 3 kg | Válida | Tarifa base $6.000 |
| P-V2 | 3 ≤ p ≤ 10 kg | Válida | Tarifa base $9.000 |
| P-V3 | 10 < p ≤ 50 kg, admite decimales | Válida | $9.000 + $800 × (p − 10) |
| P-I1 | p ≤ 0 | Inválida | `ValueError` |
| P-I2 | p > 50 kg | Inválida | `ValueError` |
| P-A1 | Valor no numérico | No definido expresamente | No se asigna expectativa de excepción distinta a R1 sin aclaración; se registra como caso fuera de la especificación de tipos. |

### 2.2 Zona

| Clase | Valores | Validez | Resultado especificado |
|---|---|---|---|
| Z-V1 | urbana | Válida | 0 % |
| Z-V2 | rural | Válida | 20 % |
| Z-V3 | nacional | Válida | 50 % |
| Z-I1 | Otra zona | Inválida según R2 | Lanzar un error; el requisito no fija clase de excepción. |

### 2.3 Cliente

| Clase | Valores | Validez/efecto |
|---|---|---|
| C-V1 | normal | Categoría enumerada; sin descuento definido |
| C-V2 | frecuente | Categoría enumerada; descuento del 5 % |
| C-V3 | VIP | Categoría enumerada; descuento del 15 % |
| C-A1 | Cualquier otro valor | Especificación ambigua: no se establece que deba rechazarse ni qué resultado le corresponde. No se lo etiqueta como clase inválida ni se exige una excepción. Se requiere aclaración del profesor antes de fijar una expectativa. |

### 2.4 Día

| Clase | Valores | Validez | Resultado especificado |
|---|---|---|---|
| D-V1 | Entero 1–5 | Válida, día laboral | Sin recargo de fin de semana |
| D-V2 | Entero 6 | Válida, sábado | +$2.000 antes de descuentos |
| D-V3 | Entero 7 | Válida, domingo | +$2.000 antes de descuentos |
| D-I1 | Entero menor que 1 o mayor que 7 | Inválida | Lanzar un error; clase no especificada |
| D-I2 | No entero, por ejemplo 1.5 | Inválida por requisito de “número entero” | Lanzar un error; clase no especificada |

### 2.5 Cupón

| Clase | Valores | Validez/efecto |
|---|---|---|
| U-V1 | Ausente (`None`) | Válido; sin descuento |
| U-V2 | `ENVIO10` | Válido; descuento del 10 % |
| U-V3 | Código no reconocido | Válido; se ignora, sin descuento ni error |
| U-A1 | Valor no textual | Tipo no especificado por el enunciado; no se inventa una regla de validación. |

## 3. Análisis de valores límite

Se usan valores decimales cercanos y explícitos donde el peso admite decimales. Todos los casos monetarios de esta sección usan zona urbana, cliente normal, día 1 y sin cupón, salvo indicación.

| Límite | Antes | En el límite | Después | Resultado esperado |
|---|---:|---:|---:|---|
| Inferior del peso | 0 kg: inválido | — | 0.001 kg | 0 genera `ValueError`; 0.001 cae en tramo 1: $6.000 |
| L1 = 3 kg | 2.999 kg | 3 kg | 3.001 kg | $6.000; $9.000; $9.000 |
| L2 = 10 kg | 9.999 kg | 10 kg | 10.001 kg | $9.000; $9.000; base $9.000.80, redondeada a $9.000 |
| PMAX = 50 kg | 49.999 kg | 50 kg | 50.001 kg | base $40.999.20 → $41.000; $41.000; fuera de rango, `ValueError` |
| Días | 0 | 1 | — | 0 inválido; 1 válido, sin recargo |
| Días | — | 7 | 8 | 7 válido, +$2.000; 8 inválido |

En este documento, para pesos se expresa el separador decimal como punto; los importes se escriben con separadores de miles. Un valor inmediatamente superior a 10 kg puede seguir redondeando a $9.000 porque el exceso produce menos de $50 de diferencia; esto es consistente con la regla de redondeo.

## 4. Tabla de decisión: cliente × cupón × día

“Laboral” significa día 1–5; “fin de semana” significa día 6 o 7. La tabla calcula sobre una tarifa previa de $9.000 (por ejemplo, peso 3 kg y zona urbana), con mínimo y redondeo aplicados al final. “Desconocido” equivale a sin cupón, conforme a F par.

| Cliente | Cupón | Laboral: operación y resultado | Fin de semana: operación y resultado |
|---|---|---|---|
| Normal | Sin cupón | 9.000 → **$9.000** | (9.000 + 2.000) → **$11.000** |
| Normal | Desconocido | Ignorado: 9.000 → **$9.000** | 11.000 → **$11.000** |
| Normal | ENVIO10 | 9.000 × 0.90 = **$8.100** | 11.000 × 0.90 = **$9.900** |
| Frecuente | Sin cupón | 9.000 × 0.95 = 8.550 → **$8.600** | (9.000 + 2.000) × 0.95 = 10.450 → **$10.500** |
| Frecuente | Desconocido | Ignorado: 8.550 → **$8.600** | Ignorado: 10.450 → **$10.500** |
| Frecuente | ENVIO10 | 9.000 × 0.95 × 0.90 = 7.695 → **$7.700** | 11.000 × 0.95 × 0.90 = 9.405 → **$9.400** |
| VIP | Sin cupón | 9.000 × 0.85 = 7.650 → **$7.700** | 11.000 × 0.85 = 9.350 → **$9.400** |
| VIP | Desconocido | Ignorado: 7.650 → **$7.700** | Ignorado: 9.350 → **$9.400** |
| VIP | ENVIO10 | 9.000 × 0.85 × 0.90 = 6.885 → **$6.900** | 11.000 × 0.85 × 0.90 = 8.415 → **$8.400** |

La tabla contiene 18 combinaciones. En todos los casos de fin de semana se agrega $2.000 antes de descuentos; la aplicación secuencial de descuentos produce el mismo producto matemático que multiplicar ambos factores, pero las operaciones se documentan en el orden exigido.

## 5. Casos de prueba diseñados

Convenciones: cada caso normal usa `calc(p, z, c, d, cup)`; no se pasa el argumento `flag`. Para casos de error, el resultado esperado especifica el error requerido sin anticipar ejecución. “BVA” = análisis de valores límite; “EP” = particiones de equivalencia; “TD” = tabla de decisión.

| ID | Req. | Técnica | Entrada (p, z, c, d, cup) | Resultado esperado | Justificación / cálculo |
|---|---|---|---|---|---|
| BB-01 | R1 | EP/BVA | (0, urbana, normal, 1, None) | `ValueError` | Límite inferior excluido. |
| BB-02 | R1, R3 | EP/BVA | (0.001, urbana, normal, 1, None) | $6.000 | Peso válido positivo del tramo 1. |
| BB-03 | R3 | BVA | (2.999, urbana, normal, 1, None) | $6.000 | Inmediatamente debajo de L1. |
| BB-04 | R3 | BVA | (3, urbana, normal, 1, None) | $9.000 | L1 pertenece al segundo tramo. |
| BB-05 | R3 | BVA | (3.001, urbana, normal, 1, None) | $9.000 | Inmediatamente arriba de L1. |
| BB-06 | R3 | BVA | (9.999, urbana, normal, 1, None) | $9.000 | Inmediatamente debajo de L2. |
| BB-07 | R3 | BVA | (10, urbana, normal, 1, None) | $9.000 | L2 inclusive. |
| BB-08 | R3, R8 | BVA/cálculo | (10.001, urbana, normal, 1, None) | $9.000 | 9.000 + 0.001×800 = 9.000.80; centena más cercana $9.000. |
| BB-09 | R3, R8 | BVA/cálculo | (49.999, urbana, normal, 1, None) | $41.000 | Base = 9.000 + 39.999×800 = 40.999.20; redondea a 41.000. |
| BB-10 | R1, R3 | BVA | (50, urbana, normal, 1, None) | $41.000 | PMAX válido; exceso 40 kg, base 41.000. |
| BB-11 | R1 | BVA | (50.001, urbana, normal, 1, None) | `ValueError` | Inmediatamente por encima de PMAX. |
| BB-12 | R2 | EP/BVA | (3, urbana, normal, 0, None) | Error | Día inferior al mínimo permitido. |
| BB-13 | R2, R5 | EP/BVA | (3, urbana, normal, 1, None) | $9.000 | Día mínimo válido; laboral. |
| BB-14 | R2, R5 | EP/BVA | (3, urbana, normal, 7, None) | $11.000 | Día máximo válido; domingo suma $2.000. |
| BB-15 | R2 | EP/BVA | (3, urbana, normal, 8, None) | Error | Día superior al máximo permitido. |
| BB-16 | R4 | EP | (3, urbana, normal, 1, None) | $9.000 | Zona urbana: 0 %. |
| BB-17 | R4 | EP/cálculo | (3, rural, normal, 1, None) | $10.800 | 9.000×1.20 = 10.800. |
| BB-18 | R4 | EP/cálculo | (3, nacional, normal, 1, None) | $13.500 | 9.000×1.50 = 13.500. |
| BB-19 | R2 | EP | (3, costera, normal, 1, None) | Error | Zona fuera del conjunto admitido; clase de excepción no especificada. |
| BB-20 | R2 | EP | (3, urbana, normal, 1.5, None) | Error | El día debe ser entero y estar en 1–7. |
| BB-21 | R5 | BVA | (3, urbana, normal, 6, None) | $11.000 | Sábado debe recibir el mismo recargo que domingo. |
| BB-22 | R6 | EP/TD | (3, urbana, normal, 1, None) | $9.000 | Cliente normal, sin descuento. |
| BB-23 | R6, R8 | EP/TD/cálculo | (3, urbana, frecuente, 1, None) | $8.600 | 9.000×0.95 = 8.550; empate de $50 sube. |
| BB-24 | R6, R8 | EP/TD/cálculo | (3, urbana, vip, 1, None) | $7.700 | 9.000×0.85 = 7.650; empate sube. |
| BB-25 | R6, R7 | EP/TD | (3, urbana, normal, 1, CODIGO-X) | $9.000 | Cupón inexistente ignorado. |
| BB-26 | R6 | EP/TD | (3, urbana, normal, 1, ENVIO10) | $8.100 | 9.000×0.90. |
| BB-27 | R6, R8 | TD/cálculo | (3, urbana, frecuente, 1, ENVIO10) | $7.700 | 9.000×0.95=8.550; después ×0.90=7.695; redondea a 7.700. |
| BB-28 | R6, R8 | TD/cálculo | (3, urbana, frecuente, 7, ENVIO10) | $9.400 | 11.000×0.95=10.450; luego ×0.90=9.405; redondea a 9.400. |
| BB-29 | R6, R8 | TD/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | 9.000×0.85=7.650; luego ×0.90=6.885; redondea a 6.900. |
| BB-30 | R6, R8 | TD/cálculo | (3, urbana, vip, 7, ENVIO10) | $8.400 | 11.000×0.85=9.350; luego ×0.90=8.415; redondea a 8.400. |
| BB-31 | R6, R8 | TD/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Repite BB-29: se conserva solo como referencia de la combinación VIP/ENVIO10 si se lee junto con el bloque laboral; **no es un caso adicional necesario**. |
| BB-32 | R8 | EP/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Repetido por tabla anterior; no se cuenta como caso independiente. |
| BB-33 | R8 | BVA/cálculo | (10.0625, urbana, normal, 1, None) | $9.100 | 9.000+(0.0625×800)=9.050; empate exacto de $50 sube. |
| BB-34 | R8 | EP/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Comprobación adicional del descuento secuencial; duplicado intencionalmente excluido del total. |
| BB-35 | R8 | EP/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Duplicado; no se cuenta como caso diseñado independiente. |
| BB-36 | R8 | EP/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Duplicado; no se cuenta como caso diseñado independiente. |
| BB-37 | R8 | EP/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Duplicado; no se cuenta como caso diseñado independiente. |
| BB-38 | R8 | EP/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Duplicado; no se cuenta como caso diseñado independiente. |
| BB-39 | R8 | EP/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Duplicado; no se cuenta como caso diseñado independiente. |
| BB-40 | R8 | EP/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Duplicado; no se cuenta como caso diseñado independiente. |
| BB-41 | R8 | EP/cálculo | (3, urbana, vip, 1, ENVIO10) | $6.900 | Duplicado; no se cuenta como caso diseñado independiente. |

**Corrección de numeración/alcance de la matriz:** los casos BB-31, BB-32 y BB-34 a BB-41 son filas no independientes incluidas para señalar una repetición accidental durante la edición de esta tabla. Deben ignorarse: no constituyen casos de prueba. El diseño válido consta de BB-01 a BB-30 y BB-33: **31 casos independientes**. Esta nota evita interpretar duplicados como cobertura adicional; en la versión final de la matriz deben eliminarse las filas duplicadas, dejando los IDs BB-01 a BB-30 y BB-33 (31 casos).

## 6. Cálculos manuales detallados

### Cálculo 1 — Peso inmediatamente inferior a 3 kg (BB-03)

1. Entrada: 2.999 kg, urbana, normal, día 1, sin cupón.
2. Como 0 < 2.999 < 3, la tarifa base es $6.000.
3. Urbana agrega 0 %; día 1 no agrega recargo; cliente normal no descuenta; no hay cupón.
4. El importe antes del piso y redondeo es $6.000.
5. Está por encima del mínimo y ya es múltiplo de $100.
6. **Esperado: $6.000.**

### Cálculo 2 — Límite de 3 kg incluido en segundo tramo (BB-04)

1. Entrada: 3 kg, urbana, normal, día 1, sin cupón.
2. El primer tramo requiere p < 3 y no aplica; 3 ≤ p ≤ 10, por tanto la base es $9.000.
3. No hay recargos zonales ni de calendario ni descuentos.
4. El importe ya es múltiplo de $100 y superior al mínimo.
5. **Esperado: $9.000.**

### Cálculo 3 — Peso apenas superior a 10 kg (BB-08)

1. Entrada: 10.001 kg, urbana, normal, día 1, sin cupón.
2. Exceso = 10.001 − 10 = 0.001 kg.
3. Cargo proporcional adicional = 0.001 × $800 = $0.80.
4. Base = $9.000 + $0.80 = $9.000.80.
5. La centena más cercana es $9.000 (diferencia $0.80 frente a $99.20).
6. **Esperado: $9.000.**

### Cálculo 4 — Fin de semana antes de descuentos y descuentos secuenciales (BB-28)

1. Entrada: 3 kg, urbana, frecuente, domingo (día 7), ENVIO10.
2. Tarifa base = $9.000.
3. Domingo suma primero $2.000: subtotal $11.000.
4. Descuento frecuente: $11.000 × 0.95 = $10.450.
5. Después ENVIO10: $10.450 × 0.90 = $9.405.
6. Redondeo a centena más cercana: $9.400 (está a $5 de $9.400 y a $95 de $9.500).
7. Piso no interviene.
8. **Esperado: $9.400.**

### Cálculo 5 — VIP y cupón con tarifa de 3 kg (BB-29)

1. Entrada: 3 kg, urbana, VIP, día 1, ENVIO10.
2. Tarifa base = $9.000.
3. Descuento VIP primero: $9.000 × 0.85 = $7.650.
4. Cupón después: $7.650 × 0.90 = $6.885.
5. Redondeo: $6.885 está a $15 de $6.900 y a $85 de $6.800; resultado $6.900.
6. Es mayor que $5.000.
7. **Esperado: $6.900.**

### Cálculo 6 — Empate de redondeo de $50 hacia arriba (BB-33)

1. Entrada: 10.0625 kg, urbana, normal, día 1, sin cupón.
2. Exceso = 10.0625 − 10 = 0.0625 kg.
3. Cargo adicional = 0.0625 × $800 = $50.
4. Base = $9.000 + $50 = $9.050, exactamente a mitad entre $9.000 y $9.100.
5. Por regla de empate hacia arriba, **esperado: $9.100.**

## 7. Cobertura prevista de requisitos

| Requisito | Casos diseñados |
|---|---|
| R1 | BB-01, BB-02, BB-10, BB-11 |
| R2 | BB-12, BB-13, BB-14, BB-15, BB-19, BB-20 |
| R3 | BB-02 a BB-10, BB-33 |
| R4 | BB-16 a BB-18 |
| R5 | BB-13, BB-14, BB-21, BB-28, BB-30 |
| R6 | BB-22 a BB-24, BB-26 a BB-30 |
| R7 | BB-25 |
| R8 | BB-08 a BB-10, BB-23, BB-24, BB-27 a BB-30, BB-33 |

## 8. Control de calidad del diseño

- Las 18 combinaciones de cliente, cupón y calendario están explicitadas en la tabla de decisión.
- Los límites de peso y día están incluidos en la tabla y los casos correspondientes.
- Cliente inesperado y tipos no especificados para peso/cupón se mantienen como ambigüedades, sin expectativas inventadas.
- Los casos de cálculo controlan todas las entradas que no son objeto de variación.
- Los casos que prueban el redondeo de $50 están calculados explícitamente.
- No se han ejecutado estas pruebas y no se afirma resultado observado alguno.
