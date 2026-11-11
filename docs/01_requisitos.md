# Parte 1. Requisitos y criterios de aceptación — EnvíaYa

**Estudiante:** Código 0182410122  
**Asignatura:** Ingeniería de Software I  
**Proyecto:** EnvíaYa  
**Repositorio:** [Male0523/Parcial_IS](https://github.com/Male0523/Parcial_IS)

## 1. Parámetros personalizados

Los últimos seis dígitos del código estudiantil son **410122**.

| Parámetro | Cálculo | Valor |
|---|---:|---:|
| A | Primer dígito de 410122 | 4 |
| B | Segundo dígito de 410122 | 1 |
| C | Tercer dígito de 410122 | 0 |
| D | Cuarto dígito de 410122 | 1 |
| E | Quinto dígito de 410122 | 2 |
| F | Sexto dígito de 410122 | 2 |
| PMAX | 30 + 5 × A | 50 kg |
| L1 | 2 + (B mod 3) | 3 kg |
| L2 | 10 + C | 10 kg |
| RR | 10 + 5 × (E mod 4) | 20 % |
| RN | 40 + 5 × (F mod 3) | 50 % |
| V | 10 + 5 × (A mod 3) | 15 % |
| S | 2000 + 500 × (C mod 4) | $2.000 |
| CAMBIO | (A + F) mod 3 | 0 |

**Reglas derivadas de paridad:**

- D = 1 es impar: el primer tramo se aplica para peso **menor que 3 kg**; 3 kg pertenece al tramo siguiente.
- E = 2 es par: el recargo de fin de semana se suma antes de los descuentos.
- B = 1 es impar: si coinciden descuento de cliente y cupón, se aplican ambos en secuencia: primero cliente y luego cupón.
- F = 2 es par: un cupón inexistente se ignora.

## 2. Requisitos funcionales

### R1. Validación del peso

El peso admite decimales y debe cumplir **0 < peso ≤ 50 kg**. Si no cumple, la función debe generar `ValueError`.

### R2. Validación de zona y día

La zona debe ser una de las zonas admitidas por la regla vigente (urbana, rural o nacional). El día debe ser un entero de 1 a 7. Si la zona no es válida o el día está fuera del rango, la función debe lanzar un error.

El requisito no prescribe una clase de excepción concreta para estos errores. La validación del tipo de cliente tampoco está especificada como requisito de error; véase la ambigüedad documentada en la sección 5.

### R3. Tarifa base

- Si el peso es menor que L1 (3 kg): **$6.000**.
- Si el peso está entre L1 (3 kg) y L2 (10 kg), inclusive: **$9.000**.
- Si supera L2 (10 kg): **$9.000 + $800 por cada kilogramo adicional**, proporcional al exceso de peso.

### R4. Recargo por zona

- Urbana: 0 %.
- Rural: RR = 20 %.
- Nacional: RN = 50 %.

### R5. Recargo de fin de semana

Sábado corresponde al día 6 y domingo al día 7. Para ambos se agrega S = **$2.000**. Por E par, este recargo se incorpora antes de aplicar los descuentos.

### R6. Descuentos

- Cliente frecuente: 5 %.
- Cliente VIP: V = 15 %.
- Cupón ENVIO10: 10 %.
- Si coinciden descuento de cliente y cupón, se aplican secuencialmente: primero el descuento de cliente y después el cupón.

### R7. Cupón inexistente

Un cupón no reconocido se ignora: no genera descuento ni error.

### R8. Costo mínimo y redondeo

El costo final no puede ser inferior a **$5.000**. Se redondea al múltiplo de $100 más cercano; los valores terminados exactamente en $50 se redondean hacia arriba.

## 3. Historias de usuario y criterios de aceptación

### HU-01. Cotizar por peso y zona

**Como** cliente de EnvíaYa, **quiero** cotizar un envío por peso y zona, **para** conocer la tarifa aplicable.

- **Dado** un peso válido menor que 3 kg, **cuando** se calcula la tarifa base, **entonces** es $6.000.
- **Dado** un peso válido entre 3 kg y 10 kg inclusive, **cuando** se calcula la tarifa base, **entonces** es $9.000.
- **Dado** un peso válido superior a 10 kg, **cuando** se calcula la tarifa base, **entonces** se agregan $800 por kilogramo proporcional que exceda 10 kg.
- **Dado** un peso menor o igual a 0 kg o superior a 50 kg, **cuando** se solicita una cotización, **entonces** se genera `ValueError`.
- **Dado** un envío rural o nacional, **cuando** se aplica el recargo zonal, **entonces** se agrega respectivamente 20 % o 50 %.

### HU-02. Considerar día y descuentos

**Como** cliente de EnvíaYa, **quiero** que la cotización considere el día, mi categoría de cliente y un cupón, **para** obtener el costo con los recargos y descuentos definidos.

- **Dado** un envío en día 6 o 7, **cuando** se calcula el costo, **entonces** se agregan $2.000 antes de los descuentos.
- **Dado** un cliente frecuente o VIP, **cuando** se calcula el costo, **entonces** se aplica respectivamente 5 % o 15 % de descuento.
- **Dado** el cupón ENVIO10, **cuando** se calcula el costo, **entonces** se aplica 10 % de descuento.
- **Dado** que coinciden un descuento de cliente y ENVIO10, **cuando** se calcula el costo, **entonces** se aplican ambos en orden secuencial, cliente primero.
- **Dado** un cupón desconocido, **cuando** se calcula el costo, **entonces** se ignora sin descuento ni error.

### HU-03. Validar entradas y entregar un costo normalizado

**Como** usuario de la calculadora, **quiero** que se validen los datos especificados y que el resultado respete el mínimo y redondeo, **para** recibir una cotización consistente.

- **Dado** una zona no admitida o un día que no sea un entero de 1 a 7, **cuando** se solicita una cotización, **entonces** se lanza un error.
- **Dado** un costo calculado inferior a $5.000, **cuando** se obtiene el costo final, **entonces** se devuelve $5.000.
- **Dado** un costo final que requiere redondeo, **cuando** se devuelve el resultado, **entonces** se usa el múltiplo de $100 más cercano y los empates de $50 se redondean hacia arriba.

## 4. Comprobación de requisitos y trazabilidad

La comprobación se hará con casos de prueba identificados en la Parte 3. La siguiente matriz deja preparadas las relaciones requisito–historia; los IDs se completarán al aprobar el diseño de casos. No representa resultados de ejecución.

| Requisito | Comprobación prevista | Historia | Casos de prueba |
|---|---|---|---|
| R1 | Probar pesos 0, menor que 0, mayor que 50, 50 y valores decimales válidos; comprobar valor o `ValueError` según corresponda. | HU-01, HU-03 | Pendiente: diseño de Parte 3 |
| R2 | Probar zonas admitidas y no admitida; días 1 y 7, fuera de rango y no enteros; comprobar error para entradas inválidas conforme al requisito. | HU-03 | Pendiente: diseño de Parte 3 |
| R3 | Probar inmediatamente debajo de 3, 3, inmediatamente arriba de 3; debajo de 10, 10, inmediatamente arriba de 10; y un peso superior con cálculo proporcional. | HU-01 | Pendiente: diseño de Parte 3 |
| R4 | Comparar el costo sin recargo urbano con rural +20 % y nacional +50 %, controlando las demás entradas. | HU-01 | Pendiente: diseño de Parte 3 |
| R5 | Comparar día laboral con días 6 y 7; comprobar que $2.000 se agregan antes de descuentos. | HU-02 | Pendiente: diseño de Parte 3 |
| R6 | Probar cliente frecuente, VIP y normal, cupón ENVIO10 y combinaciones cliente–cupón; calcular ambos descuentos secuencialmente. | HU-02 | Pendiente: diseño de Parte 3 |
| R7 | Probar cupón desconocido y compararlo con la misma cotización sin cupón; verificar que no hay descuento ni error. | HU-02 | Pendiente: diseño de Parte 3 |
| R8 | Probar mínimo y valores por debajo del mínimo, además de redondeo hacia abajo, hacia arriba y empate exacto de $50. | HU-03 | Pendiente: diseño de Parte 3 |

## 5. Ambigüedades y alcance de interpretación

- **Tipo de cliente:** el enunciado enumera normal, frecuente y VIP y define descuentos para frecuente y VIP. No establece expresamente que un cliente distinto de esos valores deba provocar un error. Por ello, esta especificación no añade una validación obligatoria ni fija el comportamiento para valores no enumerados. Ese caso se registrará como ambigüedad, no como defecto, salvo aclaración del profesor.
- **Excepción para zona y día:** R2 pide lanzar un error, pero no especifica el tipo concreto. Las pruebas comprobarán que se lanza una excepción, sin exigir una clase particular.
- **Redondeo:** “más cercano” con empate de $50 hacia arriba se interpreta como redondeo aritmético para importes no negativos.
- **Parámetros de identificación:** PMAX, L1, L2, RR, RN, V, S y CAMBIO proceden del código 0182410122 y prevalecen sobre valores de ejemplos genéricos.

## 6. Solicitud de cambio asignada

CAMBIO = (A + F) mod 3 = (4 + 2) mod 3 = 0. En la Parte 8 se evaluará la nueva zona **insular (San Andrés)**, con recargo de **70 %**, y la restricción de que los envíos insulares no aceptan cupones. Esta regla es una solicitud de cambio y no forma parte de la línea base original de R1–R8.

---

**Control de configuración:** la presente especificación describe los requisitos personalizados. El código heredado permanece sin cambios durante el diseño de pruebas inicial.
