# Parte 4. Diseño de pruebas de caja blanca — función heredada `calc`

**Objeto analizado:** exclusivamente `calc(p, z, c, d, cup=None, flag=False)` en el archivo original `envios.py` de la rama de trabajo.  
**Estado del análisis:** análisis estático del flujo de `envios.py`, cerrado en la Fase 3. Las pruebas P01–P15 se automatizaron y ejecutaron posteriormente como caracterización del legado; no analizan una versión refactorizada.

## 1. Convenciones del grafo

- Se modela el cortocircuito real de `p <= 0 or p > 50` con dos predicados: Python evalúa `p > 50` solo si `p <= 0` es falso.
- Los bloques secuenciales se agrupan en un nodo.
- Los caminos de error y de retorno convergen en un único nodo de salida para calcular complejidad con P=1.
- “Rama sí/no” se refiere al resultado del predicado.

## 2. Grafo de flujo de control

```mermaid
flowchart TD
    N1([1 Entrada]) --> N2{2 p <= 0?}
    N2 -- Sí --> N4[4 raise ValueError]
    N2 -- No --> N3{3 p > 50?}
    N3 -- Sí --> N4
    N3 -- No --> N5{5 p <= L1?}
    N4 --> N30([30 Salida])
    N5 -- Sí --> N6[6 t = 6000]
    N5 -- No --> N7{7 p <= L2?}
    N7 -- Sí --> N8[8 t = 9000]
    N7 -- No --> N9[9 t = 9000 + (p-L2)*800]
    N6 --> N10{10 z == urbana?}
    N8 --> N10
    N9 --> N10
    N10 -- Sí --> N11[11 t = t]
    N10 -- No --> N12{12 z == rural?}
    N11 --> N16{16 d > 6?}
    N12 -- Sí --> N13[13 sumar recargo rural]
    N12 -- No --> N14{14 z == nacional?}
    N13 --> N16
    N14 -- Sí --> N15[15 sumar recargo nacional]
    N14 -- No --> N16
    N15 --> N16
    N16 -- Sí --> N17[17 sumar recargo fin de semana]
    N16 -- No --> N18{18 c == frecuente?}
    N17 --> N18
    N18 -- Sí --> N19[19 aplicar descuento 5%]
    N18 -- No --> N20{20 c == vip?}
    N19 --> N20
    N20 -- Sí --> N21[21 aplicar descuento VIP]
    N20 -- No --> N22{22 cup != None?}
    N21 --> N22
    N22 -- Sí --> N23{23 cup == ENVIO10?}
    N22 -- No --> N25{25 t < 5000?}
    N23 -- Sí --> N24[24 aplicar descuento 10%]
    N23 -- No --> N25
    N24 --> N25
    N25 -- Sí --> N26[26 t = 5000]
    N25 -- No --> N27{27 flag?}
    N26 --> N27
    N27 -- Sí --> N28[28 imprimir costo]
    N27 -- No --> N29[29 retornar int(t/100)*100]
    N28 --> N29
    N29 --> N30
```

## 3. Nodos y aristas

| Nodo | Bloque/condición del código original |
|---|---|
| 1 | Entrada de la función |
| 2 | Primer operando de validación: `p <= 0` |
| 3 | Segundo operando, solo si el nodo 2 es falso: `p > 50` |
| 4 | `raise ValueError("peso invalido")` |
| 5 | `p <= CONFIG["L1"]` |
| 6 | Asignación `t = 6000` |
| 7 | `p <= CONFIG["L2"]` (rama alternativa de nodo 5) |
| 8 | Asignación `t = 9000` |
| 9 | Asignación proporcional para peso sobre L2 |
| 10 | `z == "urbana"` |
| 11 | Asignación redundante `t = t` |
| 12 | `z == "rural"` |
| 13 | Suma recargo rural |
| 14 | `z == "nacional"` |
| 15 | Suma recargo nacional |
| 16 | `d > 6` |
| 17 | Suma recargo de fin de semana |
| 18 | `c == "frecuente"` |
| 19 | Descuento frecuente |
| 20 | `c == "vip"` |
| 21 | Descuento VIP |
| 22 | `cup != None` |
| 23 | `cup == "ENVIO10"` |
| 24 | Descuento de cupón |
| 25 | `t < 5000` |
| 26 | Imposición del mínimo |
| 27 | `flag` |
| 28 | Impresión |
| 29 | Retorno truncado a centena |
| 30 | Salida común para retorno o excepción |

Las aristas dirigidas son:

`1→2; 2→4, 2→3; 3→4, 3→5; 4→30; 5→6, 5→7; 6→10; 7→8, 7→9; 8→10; 9→10; 10→11, 10→12; 11→16; 12→13, 12→14; 13→16; 14→15, 14→16; 15→16; 16→17, 16→18; 17→18; 18→19, 18→20; 19→20; 20→21, 20→22; 21→22; 22→23, 22→25; 23→24, 23→25; 24→25; 25→26, 25→27; 26→27; 27→28, 27→29; 28→29; 29→30.`

Conteo: **N = 30 nodos**, **E = 43 aristas**, **P = 1 componente conectado**.

## 4. Nodos predicado

Los predicados del grafo son los nodos **2, 3, 5, 7, 10, 12, 14, 16, 18, 20, 22, 23, 25 y 27**: 14 nodos. El predicado 3 corresponde al segundo operando de la expresión con OR y solo es alcanzable cuando el predicado 2 es falso.

## 5. Complejidad ciclomática

### Método 1: aristas, nodos y componentes

`V(G) = E − N + 2P = 43 − 30 + 2(1) = 15`

### Método 2: nodos predicado

`V(G) = número de nodos predicado + 1 = 14 + 1 = 15`

### Método 3: regiones

El grafo planar del diagrama tiene 15 regiones, incluida la región exterior:

`V(G) = número de regiones = 15`

Los tres métodos coinciden: **complejidad ciclomática 15**. La descomposición del OR en dos pruebas atómicas incrementa en uno el conteo frente a tratar toda la condición de peso como una única decisión abstracta.

## 6. Caminos independientes y casos que los recorren

Se propone una base de 15 caminos: una ruta base y catorce rutas que incorporan ramas adicionales. Cada ruta puede además ejecutar otras ramas ya cubiertas. Los datos se presentan como `(p,z,c,d,cup,flag)`. “costera” en P01 se usa únicamente como estímulo estructural para recorrer la rama falsa de `z == "urbana"`, `z == "rural"` y `z == "nacional"` del legado. Es una zona inválida según R2 y no representa un caso funcional aceptado. El retorno descrito para P01 es una deducción de flujo, no un resultado ejecutado.

| Camino | Ruta/ramas nuevas respecto de la base | Entrada para recorrerlo | Resultado esperado según flujo del legado |
|---|---|---|---|
| P01 | Base estructural: peso válido; >L1 y >L2; zona no coincide; laboral; cliente normal; cupón desconocido; costo sobre mínimo; flag falso | (11, costera, normal, 1, X, False) | Estructuralmente, retornaría 9.800; costera es inválida según R2 y no es una entrada funcional aceptada |
| P02 | Nodo 2 sí: peso ≤0, excepción | (-1, urbana, normal, 1, None, False) | Lanza ValueError |
| P03 | Nodo 2 no y nodo 3 sí: peso >50, excepción | (51, urbana, normal, 1, None, False) | Lanza ValueError |
| P04 | Nodo 5 sí: peso ≤L1 | (2, urbana, normal, 1, None, False) | Retorna 6.000 |
| P05 | Nodo 5 no y nodo 7 sí: L1 < peso ≤L2 | (5, urbana, normal, 1, None, False) | Retorna 9.000 |
| P06 | Nodo 10 sí: urbana | (11, urbana, normal, 1, None, False) | Retorna 9.800 |
| P07 | Nodo 10 no, nodo 12 sí: rural | (11, rural, normal, 1, None, False) | t=9.800×1.20=11.760; retorna 11.700 |
| P08 | Nodos 10 y 12 no, nodo 14 sí: nacional | (11, nacional, normal, 1, None, False) | t=9.800×1.50=14.700 |
| P09 | Nodo 16 sí: fin de semana | (11, urbana, normal, 7, None, False) | t=11.800; retorna 11.800 |
| P10 | Nodo 18 sí: frecuente | (11, urbana, frecuente, 1, None, False) | t=9.800×.95=9.310; retorna 9.300 |
| P11 | Nodo 20 sí: VIP | (11, urbana, vip, 1, None, False) | t=9.800×.85=8.330; retorna 8.300 |
| P12 | Nodo 22 no: sin cupón | (11, urbana, normal, 1, None, False) | Retorna 9.800 |
| P13 | Nodo 22 sí y nodo 23 sí: cupón válido | (11, urbana, normal, 1, ENVIO10, False) | t=9.800×.90=8.820; retorna 8.800 |
| P14 | Nodo 25 sí: costo inferior al mínimo | (0.001, urbana, vip, 1, ENVIO10, False) | t=6.000×.85×.90=4.590; se fija en 5.000 |
| P15 | Nodo 27 sí: flag verdadero | (3, urbana, normal, 1, None, True) | El legado imprime `costo: 6000` y retorna 6.000 por su condición `p <= L1`; R3 exige 9.000 para p=3 (discrepancia funcional BB-04). |

El test P01 recorre la rama falsa de comparación del cupón (código desconocido), y P12 recorre la rama de cupón ausente. P13 recorre cupón presente y válido. Así se ejercitan ambas salidas de los predicados 22 y 23.

Los importes indicados son deducciones manuales del código original para ilustrar las rutas estructurales, no resultados de ejecución. Los resultados que incumplen R2 ilustran la ruta que ofrece la implementación heredada, no una expectativa funcional válida.

## 7. Cobertura de sentencias y ramas

La suite de rutas P01–P15 está diseñada para alcanzar todas las sentencias ejecutables de la función:

- validación de peso y lanzamiento de excepción;
- tres asignaciones de tarifa;
- ramas urbana, rural y nacional, incluida la caída para zona no reconocida;
- recargo de fin de semana;
- descuentos frecuente y VIP;
- comprobación de cupón ausente, código desconocido y ENVIO10;
- condición y asignación del costo mínimo;
- condición del flag, impresión y retorno.

**Cobertura de sentencias prevista:** 100 % si todos los caminos propuestos se ejecutan y las aserciones/harness permiten completar la llamada cuando corresponda. Es un objetivo de diseño, no una medición.

Para cobertura de ramas se requiere recorrer ambas salidas de cada uno de los 14 predicados. P01–P15, tomados en conjunto, incluyen sí y no para nodos 2, 3, 5, 7, 10, 12, 14, 16, 18, 20, 22, 23, 25 y 27. **Cobertura de ramas prevista: 100 %**, pendiente de ejecutar una herramienta y verificar que instrumenta el cortocircuito del OR según este grafo. No se reporta cobertura medida.

## 8. Límite de esta fase

El análisis modela la función heredada sin alterar ni corregirla. La implementación no valida explícitamente zona ni día; esos casos de requisitos se diseñan en caja negra. No se ejecutó pytest, no se generaron métricas y no se ha iniciado la fase de automatización.
