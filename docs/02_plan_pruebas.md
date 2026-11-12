# Parte 2. Plan de pruebas — EnvíaYa

**Proyecto:** EnvíaYa  
**Asignatura:** Ingeniería de Software I  
**Estudiante:** Código 0182410122  
**Repositorio:** [Male0523/Parcial_IS](https://github.com/Male0523/Parcial_IS)  
**Línea base objeto de evaluación:** código heredado de `envios.py` en la versión inicial registrada antes de cualquier corrección.

## 1. Introducción

Este plan establece cómo se diseñarán, ejecutarán y documentarán las pruebas del cálculo de costos de envío de EnvíaYa. La evaluación contrastará el comportamiento del código con los requisitos personalizados R1–R8 de `docs/01_requisitos.md`. La solicitud de cambio para zona insular se planificará y comprobará aparte, en su fase correspondiente.

El orden de trabajo preserva la línea base: primero se completa el diseño de pruebas y se ejecuta contra el código heredado sin modificarlo; después se documentan los resultados observados; solo entonces se realizan refactorización y correcciones en fases posteriores.

## 2. Objetivos

- Comprobar que las entradas y los cálculos cumplen R1–R8.
- Diseñar pruebas reproducibles de caja negra y, sobre el código original, de caja blanca.
- Ejecutar la suite automatizada contra la línea base y registrar resultados reales, sin anticipar ni inventar hallazgos.
- Tras los cambios posteriores, ejecutar la regresión y comparar resultados con la línea base.
- Mantener trazabilidad entre requisito, historia de usuario, caso de prueba, ejecución y defecto observado.

## 3. Alcance

Se probará la función pública `calc` de `envios.py` y el cálculo que realiza para:

- peso, incluidos límites, decimales y valores inválidos (R1);
- zona y día (R2);
- tarifa por tramos y proporcionalidad sobre 10 kg (R3);
- recargos urbano, rural y nacional (R4);
- sábado y domingo, con recargo antes de descuentos (R5);
- descuentos de cliente, cupón y su orden secuencial (R6);
- cupón desconocido (R7);
- mínimo de $5.000 y redondeo a centenas, incluido empate de $50 (R8).

También se incluirán pruebas de regresión para cada caso automatizado que se confirme como válido. La cobertura de la solicitud de zona insular y su restricción de cupones pertenece a la Parte 8 y se añadirá como suite específica.

## 4. Fuera del alcance

- Interfaz gráfica, API web, persistencia, base de datos, autenticación o infraestructura de despliegue: no forman parte del repositorio evaluado.
- Rendimiento, concurrencia, seguridad y pruebas de carga: no están solicitadas por estos requisitos ni hay una plataforma de servicio que evaluar.
- Validar como error un tipo de cliente distinto de normal, frecuente o VIP: el enunciado enumera las categorías, pero no define el comportamiento de rechazo para otros valores. Se registra como ambigüedad, sin imponer una expectativa de error.
- Reglas de la zona insular en la línea base R1–R8: se evaluarán únicamente como cambio en la Parte 8.

## 5. Elementos que serán probados

1. `envios.calc(p, z, c, d, cup=None, flag=False)`, inicialmente sin modificar.
2. La salida retornada y las excepciones observables, comparadas con resultados esperados derivados manualmente de los requisitos.
3. La salida de consola del argumento `flag` solo como comportamiento legado a documentar; no se considera requisito funcional de cálculo.
4. En fases posteriores, los módulos refactorizados, sus estrategias de zona y descuento y la integración de la nueva zona insular, manteniendo las mismas expectativas funcionales para R1–R8.

## 6. Niveles de prueba

| Nivel | Aplicación a EnvíaYa | Evidencia prevista |
|---|---|---|
| Unidad | Probar `calc` con entradas individuales y combinaciones controladas: límites de peso, zona, día, cliente y cupón. | Casos unitarios en `tests/` y resultado real de pytest. |
| Integración | Comprobar que `calc` utiliza correctamente configuración, reglas de tarifas, recargos, descuentos y redondeo. En la arquitectura posterior, comprobar llamadas entre calculadora y estrategias. | Pruebas de combinación y regresión en `tests/`. |
| Sistema | Ejecutar el flujo completo disponible en el repositorio: invocar la función pública y verificar su resultado o excepción como unidad funcional del sistema entregado. No se presupone una aplicación externa. | Comando de suite completa y su salida guardada cuando exista. |
| Aceptación | Contrastar historias HU-01 a HU-03 y ejemplos de uso representativos con los criterios Dado/Cuando/Entonces. Revisar que el producto documentado y el comportamiento entregado cumplen lo acordado. | Lista de criterios vinculada a casos y revisión de resultados. |

Los niveles describen el alcance conceptual de las pruebas; dado que el repositorio contiene una función Python y no una aplicación multicapa, varias comprobaciones se ejecutarán técnicamente como pruebas automatizadas de función.

## 7. Estrategia de pruebas

### 7.1 Diseño

- **Caja negra:** particiones de equivalencia, análisis de límites y tabla de decisión. La matriz de al menos 20 casos se prepara en `docs/03_caja_negra.md`.
- **Caja blanca:** analizar el flujo de la versión original, derivar complejidad ciclomática y caminos independientes antes de refactorizar; documentar en `docs/04_caja_blanca.md`.
- **Automatización:** pytest para ejecución y aserciones; pytest-cov para cobertura de sentencias y ramas cuando la versión/configuración instalada lo soporte.
- **Oráculo:** calcular cada resultado esperado a partir de R1–R8 y los parámetros A–F; revisar manualmente los cálculos antes de usarlos como expectativas.
- **Secuencia:** diseño → ejecución contra legado intacto → registro de resultados y defectos observados → corrección/refactorización → regresión. Las pruebas nuevas para insular se escriben y ejecutan antes de implementar ese cambio.
- **Regresión:** reutilizar las mismas expectativas funcionales después de corregir; distinguir claramente pruebas de requisitos originales y pruebas de la solicitud insular.

### 7.2 Técnicas y datos

- Valores límite de peso: 0, valores positivos cercanos a 0, inmediatamente debajo de 3, 3, inmediatamente arriba de 3, inmediatamente debajo de 10, 10, inmediatamente arriba de 10, 50 e inmediatamente arriba de 50.
- Valores representativos de zona: urbana, rural, nacional y una zona no admitida.
- Días: 1, 5, 6, 7, 0, 8 y valores no enteros.
- Cliente: normal, frecuente y VIP. Un valor no enumerado se documenta como ambigüedad; no se fija un resultado requerido.
- Cupón: ausente, ENVIO10 y código no reconocido.
- Combinaciones de descuentos: categoría de cliente con cupón, y día laboral/fin de semana; el recargo de fin de semana precede a descuentos.
- Redondeo: valores calculados por debajo/encima de una centena y exactamente a $50 de la centena más cercana; revisar piso de $5.000.

La matriz concreta indicará datos, resultado esperado, requisito, técnica y justificación. Cada cálculo manual tendrá operaciones explícitas para evitar usar como oráculo el resultado del código bajo prueba.

## 8. Ambiente y herramientas

Ambiente previsto: GitHub Codespaces o entorno local compatible, con el repositorio clonado y Python disponible. Las versiones exactas de Python y dependencias se registrarán al ejecutar; no se presuponen ni se reportan en este plan.

Herramientas:

- Python para ejecutar el código.
- pytest para descubrir y ejecutar pruebas.
- pytest-cov para medir cobertura de sentencias y ramas.
- Git para conservar la línea base, ramas, commits y cambios por fase.
- Markdown para casos, trazabilidad, defectos y evidencias textuales.

Comandos previstos desde la raíz del repositorio (se ejecutarán cuando estén configuradas las dependencias):

```bash
python --version
python -m pip install -r requirements.txt
python -m pytest -q
python -m pytest --cov=envios --cov-branch --cov-report=term-missing
```

Si el proyecto todavía no contiene `requirements.txt`, la instalación se ajustará en la fase de automatización y se documentará el cambio antes de ejecutar. Las salidas y métricas solo se incorporarán después de una ejecución real.

## 9. Roles y responsabilidades

| Rol | Responsabilidad |
|---|---|
| Estudiante / responsable del proyecto | Mantener requisitos y trazabilidad, revisar cálculos esperados, ejecutar los comandos, conservar evidencias y explicar los resultados. |
| Diseñador de pruebas | Derivar particiones, límites, decisiones y caminos desde los requisitos y el código heredado; proponer casos con IDs únicos. |
| Implementador | Mantener intacta la línea base durante el diseño inicial; en fases posteriores corregir solo defectos demostrados y conservar compatibilidad según la decisión documentada. |
| Revisor académico | Verificar que las reglas personalizadas, las técnicas y las conclusiones coincidan con el enunciado y que no se presenten datos no ejecutados como resultados. |

En este proyecto académico una misma persona puede desempeñar varios roles; la tabla separa responsabilidades para que sean verificables.

## 10. Comprobación requisito por requisito

| Requisito | Cómo se comprobará | Evidencia/casos |
|---|---|---|
| R1 | Probar 0, negativos, valores entre 0 y 50, 50 y mayores que 50; esperar `ValueError` solo fuera del intervalo y un cálculo para pesos válidos. Incluir decimales. | Casos de límites de peso en la matriz de caja negra y pruebas automatizadas. |
| R2 | Probar cada zona permitida, una zona no permitida, días 1 y 7, días fuera del rango y un día no entero. Para entradas inválidas se espera una excepción, sin exigir una clase concreta porque el requisito no la define. | Casos de partición de zona/día y pruebas automatizadas. |
| R3 | Probar debajo/igual/encima de 3 y 10 kg; verificar tarifas de $6.000 y $9.000 y cálculo proporcional de $800/kg por exceso de 10 kg. | Casos de valores límite y cálculos manuales. |
| R4 | Comparar zona urbana con rural y nacional, verificando porcentajes de 0 %, 20 % y 50 % manteniendo constantes las otras entradas. | Casos de zona y cálculos derivados. |
| R5 | Comparar días laborales, sábado 6 y domingo 7; verificar que ambos días de fin de semana suman $2.000 antes de descuentos. | Casos de decisión y pruebas de orden de operaciones. |
| R6 | Probar cliente normal, frecuente y VIP; ENVIO10; y combinación de cliente con cupón. Calcular porcentajes secuencialmente en orden cliente y luego cupón. | Tabla de decisión y casos de descuento. |
| R7 | Comparar el mismo envío con cupón ausente y con cupón desconocido; el desconocido debe producir el mismo efecto que ninguno, sin error. | Casos de cupón y prueba de no regresión. |
| R8 | Probar el mínimo con y sin descuentos; valores que deban redondear hacia abajo, arriba y empate de $50 hacia arriba. | Casos de piso y redondeo, con cálculo esperado independiente. |

## 11. Riesgos y mitigaciones

| Riesgo | Efecto posible | Mitigación |
|---|---|---|
| Confundir comportamiento legado con requisito | Falsos defectos o expectativas incorrectas | Derivar cada aserción desde R1–R8; separar hallazgo observado de interpretación. |
| Alterar el código antes de la primera ejecución | Se pierde la evidencia del comportamiento original | Conservar `envios.py` intacto hasta ejecutar la suite diseñada y guardar la referencia de línea base. |
| Cálculo esperado copiado de la función probada | La prueba reproduce el mismo error | Usar cálculo manual independiente y revisar operaciones antes de automatizar. |
| Tipo de excepción no especificado para R2 | Prueba demasiado restrictiva | Afirmar que se lanza una excepción sin requerir clase específica. |
| Tipo de cliente no definido para valores inesperados | Falso requisito de validación | Registrar la ambigüedad; no exigir error hasta aclaración del profesor. |
| Diferencias de versión o dependencias | Pruebas no reproducibles | Registrar versión de Python y dependencias instaladas en la evidencia de ejecución. |
| Redondeo binario de valores decimales | Resultados centavo/múltiplo incorrectos en límites | Diseñar expectativas con importes reproducibles y revisar casos exactos de empate; registrar el método usado. |
| Reportar métricas sin ejecución | Informe no verificable | Completar porcentajes, defectos y cobertura solo con salidas reales guardadas. |

## 12. Criterios de entrada

- Requisitos R1–R8 y parámetros personalizados revisados.
- Código heredado identificado y sin modificaciones funcionales.
- Casos de caja negra diseñados con entradas y resultados esperados revisados manualmente.
- Casos de caja blanca derivados de la versión original.
- Python disponible y dependencias instalables en el entorno seleccionado.
- Rama de trabajo y estado de Git identificados para preservar los cambios.

## 13. Criterios de salida

- Todos los casos diseñados tienen ID, requisito, datos, resultado esperado, justificación y técnica.
- Se ejecutó la suite contra la línea base y se conservó su salida real; los fallos se registran como observaciones, sin afirmar que son defectos hasta contrastarlos con los requisitos.
- Cada defecto reportado tiene pasos reproducibles, requisito incumplido y resultado observado documentado.
- Se reportan métricas solo si se generaron mediante ejecución real y se indica el comando usado.
- Después de correcciones, se ejecuta la regresión y se comparan los resultados antes/después.
- La matriz de trazabilidad vincula R1–R8 con historias y IDs de casos; toda brecha está marcada como pendiente o ambigüedad.
- La solicitud insular se prueba en su fase y se mantiene distinguida de la línea base R1–R8.

## 14. Trazabilidad inicial de la Fase 2

La tabla siguiente conserva la instantánea del plan al cierre de la Fase 2: los campos pendientes describían trabajo futuro en ese momento. El diseño, automatización y resultados posteriores están en `docs/03_caja_negra.md`, `docs/04_caja_blanca.md`, `docs/05_resultados_pruebas.md` y `docs/09_informe_final.md`.

Los IDs se asignarán en `docs/03_caja_negra.md` y se copiarán aquí y en `docs/01_requisitos.md`. Hasta diseñar y ejecutar esos casos, no se atribuyen resultados.

| Requisito | Historia | Casos de caja negra | Casos de caja blanca | Automatizados | Resultado de línea base |
|---|---|---|---|---|---|
| R1 | HU-01, HU-03 | Pendiente de Parte 3 | Pendiente de análisis real de flujo | Pendiente de Parte 5 | Pendiente de ejecución |
| R2 | HU-03 | Pendiente de Parte 3 | Pendiente de análisis real de flujo | Pendiente de Parte 5 | Pendiente de ejecución |
| R3 | HU-01 | Pendiente de Parte 3 | Pendiente de análisis real de flujo | Pendiente de Parte 5 | Pendiente de ejecución |
| R4 | HU-01 | Pendiente de Parte 3 | Pendiente de análisis real de flujo | Pendiente de Parte 5 | Pendiente de ejecución |
| R5 | HU-02 | Pendiente de Parte 3 | Pendiente de análisis real de flujo | Pendiente de Parte 5 | Pendiente de ejecución |
| R6 | HU-02 | Pendiente de Parte 3 | Pendiente de análisis real de flujo | Pendiente de Parte 5 | Pendiente de ejecución |
| R7 | HU-02 | Pendiente de Parte 3 | Pendiente de análisis real de flujo | Pendiente de Parte 5 | Pendiente de ejecución |
| R8 | HU-03 | Pendiente de Parte 3 | Pendiente de análisis real de flujo | Pendiente de Parte 5 | Pendiente de ejecución |

---

**Estado del plan:** diseñado para orientar las siguientes fases. No se han ejecutado pruebas ni calculado métricas mediante este documento.
