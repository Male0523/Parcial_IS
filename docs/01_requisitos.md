# Parte 1. Requisitos y criterios de aceptación — EnvíaYa

**Estudiante:** Código 0182410122  
**Asignatura:** Ingeniería de Software I  
**Repositorio:** Parcial_IS

## 1. Parámetros personalizados

Los seis últimos dígitos del código estudiantil son **410122**:

| Variable | Cálculo | Valor |
|---|---:|---:|
| A | 4 | 4 |
| B | 1 | 1 |
| C | 0 | 0 |
| D | 1 | 1 |
| E | 2 | 2 |
| F | 2 | 2 |
| PMAX | 30 + 5 × A | 50 kg |
| L1 | 2 + (B mod 3) | 3 kg |
| L2 | 10 + C | 10 kg |
| RR | 10 + 5 × (E mod 4) | 20 % |
| RN | 40 + 5 × (F mod 3) | 50 % |
| V | 10 + 5 × (A mod 3) | 15 % |
| S | 2000 + 500 × (C mod 4) | $2.000 |
| CAMBIO | (A + F) mod 3 | 0 |

**Interpretación de paridades:**
- D = 1 es impar: el tramo 1 aplica cuando peso < 3 kg; el límite de 3 kg no se incluye.
- E = 2 es par: el recargo de fin de semana se suma antes de los descuentos.
- B = 1 es impar: cuando coinciden descuento de cliente y cupón, se aplican ambos; primero el descuento del cliente y luego el cupón.
- F = 2 es par: un cupón inexistente se ignora.

## 2. Especificación de requisitos

### R1. Validación del peso
El peso debe cumplir 0 < peso ≤ 50 kg. Si no cumple, se lanza `ValueError("peso inválido")` (el código heredado contiene el texto sin tilde: `peso invalido`).

### R2. Validación de zona y día
La zona debe ser urbana, rural o nacional. El día debe ser un entero entre 1 y 7; 6 corresponde al sábado y 7 al domingo. Si la zona o el día no son válidos, se lanza un error.

### R3. Tarifa base por tramos
- Tramo 1: $6.000 cuando peso < 3 kg.
- Tramo 2: $9.000 cuando 3 kg ≤ peso ≤ 10 kg.
- Por encima de 10 kg: $9.000 + $800 por cada kilogramo que exceda 10 kg, proporcionalmente.

### R4. Recargo por zona
- Urbana: sin recargo.
- Rural: +20 %.
- Nacional: +50 %.

### R5. Recargo de fin de semana
Para sábado (día 6) y domingo (día 7), se agregan $2.000. Por E = 2 (par), este recargo se suma antes de aplicar descuentos.

### R6. Descuentos
- Cliente frecuente: 5 %.
- Cliente VIP: 15 %.
- Cupón ENVIO10: 10 %.
- Como B = 1 (impar), si coinciden descuento del cliente y cupón, se aplican ambos secuencialmente: primero cliente y después cupón.

### R7. Cupón inexistente
Como F = 2 (par), un cupón que no exista se ignora; no genera error ni descuento.

### R8. Piso y redondeo
El costo final no puede ser inferior a $5.000. El resultado se redondea al múltiplo de $100 más cercano; los valores terminados en $50 se redondean hacia arriba.

## 3. Historias de usuario y criterios de aceptación

### HU-01. Calcular tarifa según peso y zona
**Como** cliente de EnvíaYa, **quiero** cotizar un envío indicando su peso y zona, **para** conocer la tarifa base y los recargos aplicables.

- **Dado** un peso mayor que 0 y menor que 3 kg, **cuando** solicito una cotización, **entonces** la tarifa base es $6.000.
- **Dado** un peso de 3 kg o superior y hasta 10 kg, **cuando** solicito una cotización, **entonces** la tarifa base es $9.000.
- **Dado** un peso superior a 10 kg y no mayor que 50 kg, **cuando** solicito una cotización, **entonces** se suman $800 por cada kilogramo proporcional que exceda 10 kg a la base de $9.000.
- **Dado** un peso fuera del intervalo permitido, **cuando** solicito una cotización, **entonces** el sistema lanza un error de peso inválido.
- **Dado** un envío rural o nacional, **cuando** se calcula su tarifa, **entonces** se aplica respectivamente un recargo del 20 % o del 50 %.

### HU-02. Aplicar calendario y descuentos
**Como** cliente de EnvíaYa, **quiero** que la cotización considere el día, mi tipo de cliente y mi cupón, **para** obtener el costo correspondiente.

- **Dado** un envío programado para sábado o domingo, **cuando** se calcula su costo, **entonces** se agregan $2.000 antes de los descuentos.
- **Dado** un cliente frecuente, **cuando** cotiza, **entonces** recibe un descuento del 5 %.
- **Dado** un cliente VIP, **cuando** cotiza, **entonces** recibe un descuento del 15 %.
- **Dado** un cupón ENVIO10 válido, **cuando** se aplica, **entonces** se descuenta un 10 %.
- **Dado** que coinciden descuento de cliente y cupón, **cuando** se calcula el costo, **entonces** ambos descuentos se aplican secuencialmente, primero cliente y luego cupón.
- **Dado** un cupón inexistente, **cuando** se calcula el costo, **entonces** el cupón se ignora.

### HU-03. Validar y entregar un costo consistente
**Como** responsable de calidad del sistema, **quiero** que se validen los datos de entrada y se normalice el costo final, **para** evitar cotizaciones inválidas o inconsistentes.

- **Dado** una zona distinta de urbana, rural o nacional, **cuando** se solicita una cotización, **entonces** se lanza un error.
- **Dado** un día fuera del intervalo 1 a 7, **cuando** se solicita una cotización, **entonces** se lanza un error.
- **Dado** un costo calculado inferior a $5.000, **cuando** se obtiene el resultado final, **entonces** el costo se establece en $5.000.
- **Dado** un costo que debe normalizarse, **cuando** se devuelve el resultado, **entonces** se redondea al múltiplo de $100 más cercano y los $50 se redondean hacia arriba.

## 4. Matriz inicial de trazabilidad

Los identificadores de casos se asignarán en la Parte 3 y se completarán con los resultados de ejecución en la Parte 5.

| Requisito | Historia de usuario | Casos de prueba |
|---|---|---|
| R1 | HU-01, HU-03 | Pendiente de diseño (Parte 3) |
| R2 | HU-03 | Pendiente de diseño (Parte 3) |
| R3 | HU-01 | Pendiente de diseño (Parte 3) |
| R4 | HU-01 | Pendiente de diseño (Parte 3) |
| R5 | HU-02 | Pendiente de diseño (Parte 3) |
| R6 | HU-02 | Pendiente de diseño (Parte 3) |
| R7 | HU-02 | Pendiente de diseño (Parte 3) |
| R8 | HU-03 | Pendiente de diseño (Parte 3) |

## 5. Solicitud de cambio asignada

CAMBIO = (4 + 2) mod 3 = 0. Corresponde incorporar la zona **insular (San Andrés)** con recargo del **70 %**. Los envíos insulares no aceptan cupones. Este cambio se analizará e implementará en la Parte 8, en una rama independiente y con pruebas escritas primero.

---
**Nota de control:** esta especificación representa las reglas personalizadas del estudiante. El código heredado se conserva inicialmente sin corregir para que las pruebas permitan identificar sus defectos antes de la refactorización.
