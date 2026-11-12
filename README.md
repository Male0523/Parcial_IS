# EnvíaYa

Calculadora académica de costos de envío desarrollada para el parcial de Ingeniería de Software I. Recibe peso, zona, categoría de cliente, día de la semana y cupón opcional. Aplica las tarifas y validaciones personalizadas, recargos, descuentos, mínimo y redondeo definidos en los requisitos. La versión activa admite las zonas urbana, rural, nacional e insular (San Andrés).

## Requisitos

- Python 3.12 (la versión usada por GitHub Actions).
- pip.
- Los paquetes de prueba declarados en `requirements.txt`: pytest y pytest-cov.

## Instalación

Desde la raíz del repositorio:

```bash
python -m venv .venv
```

Activa el entorno virtual:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

Instala dependencias:

```bash
python -m pip install -r requirements.txt
```

## Pruebas

Ejecuta desde la raíz. `pytest.ini` configura la ruta de importación raíz para que funcionen tanto el módulo heredado `envios` como el paquete activo `src`.

```bash
python -m pytest -q tests/
pytest -q tests/
python -m pytest -q tests/ --cov=src --cov-branch --cov-report=term-missing
```

Para guardar los reportes JUnit y JSON de cobertura que conserva CI, el workflow genera los reportes como artefactos de cada ejecución de GitHub Actions. No se debe interpretar una configuración local como evidencia de que una ejecución de Actions terminó correctamente; consulta el estado de los runs en GitHub.

## Estructura

```text
.
├── .github/workflows/tests.yml  # Integración continua y artefactos
├── docs/                       # Requisitos, pruebas, resultados e informes
├── envios.py                   # Implementación heredada preservada para análisis
├── evidencias/                  # Evidencias generadas por CI, cuando existan
├── src/
│   ├── calculadora.py           # Validaciones y contexto del cálculo
│   ├── configuracion.py         # Constantes de dominio
│   └── estrategias_zona.py      # Estrategias por zona (Strategy)
├── tests/
│   ├── test_caja_negra.py
│   ├── test_caja_blanca.py
│   ├── test_regresion.py
│   └── test_zona_insular.py
├── pytest.ini
└── requirements.txt
```

## Arquitectura

La API activa es `src.calculadora.calc(peso, zona, cliente, dia, cup=None)`. El contexto `CalculadoraEnvios` valida las entradas y coordina el cálculo; las estrategias `ZonaUrbana`, `ZonaRural`, `ZonaNacional` y `ZonaInsular` encapsulan el recargo y la política de cupones de cada zona. `envios.py` se conserva como línea base histórica y se usa para caracterización estructural, no como implementación de la nueva función funcional.

## Documentación

- [Informe final](docs/09_informe_final.md)
- [Requisitos y criterios de aceptación](docs/01_requisitos.md)
- [Plan de pruebas](docs/02_plan_pruebas.md)
- [Resultados históricos de Fase 4](docs/05_resultados_pruebas.md)
- [Refactorización](docs/06_refactorizacion.md)
- [Cambio de zona insular](docs/08_cambio_insular.md)
