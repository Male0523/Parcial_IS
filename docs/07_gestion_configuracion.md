# Fase 6. Gestión de configuración y versionamiento

## 1. Auditoría inicial

La auditoría remota del 11 de noviembre de 2026 encontró estas ramas antes de iniciar la integración:

| Rama | Commit observado | Contenido relevante |
|---|---|---|
| `main` | `545ec593b004112d0bda6f8b71d62a2f8d9866df` | Código heredado y requisitos iniciales |
| `docs/fase-2-plan-pruebas` | `37dd270029a49ab0d62de4899c8e20f01228aec8` | Fases 1–4, BB-01–BB-41, P01–P15, informe histórico |
| `refactor/estrategia` | `9b7c1b03d3a533b9d51a85849f606c902ef1fc72` | Fases anteriores, refactor, regresión y documentación Fase 5 |

No existían ramas `test/suite`, `fix/DEF-01` a `fix/DEF-04`, etiquetas ni PR anteriores en la auditoría. El commit inicial `3ffcbe0` contiene la primera versión; `8fdc6625efaffb39dcb70d57c9495503fc096306` registra la versión heredada con parámetros personalizados. El blob original de `envios.py` es `5585b110170a271dadc20c11d67f8c62fb9a0b3c`. La rama refactor conserva ese archivo sin modificación y mantiene los resultados de Fase 4 en `docs/05_resultados_pruebas.md`.

En `refactor/estrategia` se verificaron `src/calculadora.py`, `src/configuracion.py`, `src/estrategias_zona.py`, `docs/06_refactorizacion.md` y las tres suites de pruebas. La documentación de Fase 5 registra 63 aprobadas, 0 fallidas y 100% de sentencias y ramas sobre `src/` en Actions run 43109179938.

## 2. Estrategia de ramas e integración

- `main` es la rama integrada de entrega.
- `docs/fase-2-plan-pruebas` conserva el historial de requisitos, diseño y ejecución de la línea base.
- `test/suite` se creó en el commit histórico `37dd270`; contiene los 41 IDs BB y los 15 caminos P sin commits adicionales o reescritura. Su PR #1 fue comparado contra `main` (17 commits adelante, 0 atrás, sin conflictos) y se integró con merge commit `24dd66794b604dfb938a6fba0759f14c1d74a1de`.
- `refactor/estrategia` retiene su historial posterior a pruebas y su separación del código heredado. El PR #2 se integró después de revisar la comparación y `mergeable: true`, mediante el merge commit `af258871346022904ebdf8fac7bfb629464bcea3`.
- No se empleó force push ni se borraron ramas o commits.

### Ramas fix/DEF

No había evidencia de ramas `fix/DEF-01`, `fix/DEF-02`, `fix/DEF-03` ni `fix/DEF-04`. La Fase 5 corrigió los cuatro defectos dentro de commits reales de `refactor/estrategia` junto con la arquitectura modular; no aisló cada corrección en una rama ni un commit por defecto. Para no falsear el historial, esta fase no crea ramas vacías ni reconstruye commits artificiales. La trazabilidad se conserva mediante el mapeo DEF → casos BB en `docs/06_refactorizacion.md`, el historial original y la rama refactorizada. Si el curso requiere estrictamente ramas separadas, deberán desarrollarse como trabajo nuevo desde una base acordada, con cambios reales y PRs nuevos; no se pueden presentar como historial de Fase 5.

## 3. Etiquetas y releases

La auditoría de inicio de Fase 6 no encontró etiquetas. Una verificación posterior confirmó que `v1.0.0` ya existe como etiqueta anotada: el objeto de etiqueta `36f9119002981d0c856d9da0b5958f20c158d53f` apunta directamente al commit `8fdc6625efaffb39dcb70d57c9495503fc096306`, que contiene el código heredado. No apunta a la refactorización. En esa verificación, `v1.1.0` figuraba en el changelog pero no como etiqueta. Para inspeccionar el destino:

```bash
git fetch origin --tags
git cat-file -p v1.0.0
git rev-parse v1.0.0^{commit}
```

El último comando debe mostrar `8fdc6625efaffb39dcb70d57c9495503fc096306`.

## 4. Versionamiento semántico

La referencia heredada es `envios.calc(p, z, c, d, cup=None, flag=False)`; la nueva función es `src.calculadora.calc(peso, zona, cliente, dia, cup=None)`. Los nombres de parámetros cambian, `flag` desaparece y la ruta de importación nueva es distinta.

La rama refactor conserva el módulo `envios` y su firma para caracterizar el comportamiento anterior; añade un módulo de calculadora separado en `src`. Por tanto, el cambio versionado aquí es una nueva entrada modular compatible por adición para los consumidores que sigan usando `envios.calc`. Se registra como **1.1.0** (mejora compatible), no como ruptura automática. Un consumidor que migre a `src.calculadora.calc` sí debe ajustar su importación y dejar de pasar `flag`; esas instrucciones de migración se documentan en las notas de versión.

Si el proyecto declara en el futuro que `src.calculadora.calc` reemplaza oficialmente `envios.calc` y elimina el módulo/firma heredados, ese cambio contractual sí requiere un major (por ejemplo, 2.0.0). No se afirma que esa eliminación haya ocurrido en esta fase.

## 5. Historial y evidencia Git

Los commits observados son descriptivos y cronológicamente conservados. La topología comprobada por SHA y padres es: línea inicial `3ffcbe0 → 8fdc662 → 545ec59`; los 17 commits de Fases 1–4 concluyen en `37dd270`; refactor/estrategia parte de `37dd270` y agrega sus commits Fase 5. La suite se integró a main mediante el merge `24dd667`, sin squash y preservando ambos padres. La salida completa local se obtiene con:

```bash
git log --oneline --graph --all
```

Para confirmar ramas, etiqueta y estado:

```bash
git fetch --all --tags
git branch -a
git tag --list
git show --no-patch --format="%H %D" v1.0.0
git log --oneline --graph --all
```

La vista por ramas también está disponible en GitHub: [commits main](https://github.com/Male0523/Parcial_IS/commits/main), [commits suite](https://github.com/Male0523/Parcial_IS/commits/test/suite), [commits refactor](https://github.com/Male0523/Parcial_IS/commits/refactor/estrategia) y [PR #1](https://github.com/Male0523/Parcial_IS/pull/1).

## 6. Integración y validación

La integración y resultados de Fase 5 se registran sin alterar la línea base de Fase 4. El contenido heredado de `envios.py` conserva blob SHA `5585b110170a271dadc20c11d67f8c62fb9a0b3c`; la verificación local en Codespaces es:

```bash
git show 8fdc6625efaffb39dcb70d57c9495503fc096306:envios.py | sha1sum
git show main:envios.py | sha1sum
python -m pytest -q tests/
```

La salida SHA-1 esperada para ambos archivos es `5585b110170a271dadc20c11d67f8c62fb9a0b3c`. GitHub Actions ejecutó el comando configurado `python -m pytest -q tests/` con reporte de cobertura en run [43111064026](https://github.com/Male0523/Parcial_IS/actions/runs/43111064026), commit `56a4e4a49fb84eb062ee353d390b3e891f2856c7`, rama `refactor/estrategia`: el job `pytest` y el paso de ejecución concluyeron correctamente; la evidencia de Fase 5 documenta 63 aprobadas, 0 fallidas, 0 errores, cobertura activa 100% (99/99 sentencias, 20/20 ramas), y el artefacto `enviaya-test-evidence-43111064026` conserva JUnit, cobertura y salida. El commit `56a4e4a` solo agregó el changelog; los commits siguientes añadieron documentos. Esta sesión no dispone de checkout local de Git/Python para ejecutar el comando después del merge y no atribuye esa ejecución al commit final `af25887`. La Fase 6 no implementa la zona insular.


## 7. Estado final verificado al cierre de la Fase 6

- Ramas remotas presentes: `docs/fase-2-plan-pruebas`, `test/suite`, `refactor/estrategia` y `main`; las dos ramas de trabajo siguen conservadas.
- PR #1 y PR #2 están integrados en `main`; `main` termina en `af258871346022904ebdf8fac7bfb629464bcea3` antes de este apunte final.
- Los blobs `envios.py` en el commit heredado y en `main` se compararon: ambos tienen SHA `5585b110170a271dadc20c11d67f8c62fb9a0b3c` y contenido idéntico.
- La etiqueta anotada `v1.0.0` fue verificada: su destino es el commit heredado `8fdc6625efaffb39dcb70d57c9495503fc096306`.
- La salida literal del comando de git log debe generarse en Codespaces, porque este entorno de trabajo no tiene `git` instalado. Los hashes, mensajes y relaciones parentales aquí se leyeron del historial remoto.


## 8. Actualización de estado remoto posterior a la Fase 6

Esta sección complementa el registro histórico anterior; no reescribe el estado observado al cierre de la Fase 6.

- HEAD remoto de `main` verificado: `9967f0d4f1c9c39d380f611f65dfaf9580a66b57`. La integración más reciente en el corte de esta actualización incluye PR #6; el commit siguiente agrega evidencias versionadas.
- PR #1 a #6 están fusionados en `main`: #1 `24dd66794b604dfb938a6fba0759f14c1d74a1de`; #2 `af258871346022904ebdf8fac7bfb629464bcea3`; #3 `2db2f81d56d95930c5f35f9f63981ee4cc17c52c`; #4 `d24a703e5a571ea9646e30cf538897122cabd5e6`; #5 `c892adcc64691c5f58492de67a412225c1d3e295`; #6 `c9114b52c3fb61d6922828a7096dee01d14d499c`.
- Las etiquetas anotadas existen: `v1.0.0` → `8fdc6625efaffb39dcb70d57c9495503fc096306`; `v1.1.0` → `af258871346022904ebdf8fac7bfb629464bcea3`; `v1.2.0` → `2db2f81d56d95930c5f35f9f63981ee4cc17c52c`.
- La lista remota de ramas cambia con el tiempo; las ramas activas observadas durante esta actualización incluyen `main`, `docs/fase-2-plan-pruebas`, `docs/fase-8-informe-final`, `docs/ajuste-academico-final`, `docs/final-quality-corrections`, `chore/configuracion-mantenibilidad`, `feature/zona-insular`, `refactor/estrategia` y `test/suite`. No se encontraron ramas `fix/DEF-01` a `fix/DEF-04`; las correcciones se integraron dentro de la refactorización.
- Actions run 43127692693, sobre el HEAD entonces actual de `main`, ejecutó 75 casos por invocación; la cobertura registrada fue 110/110 sentencias y 22/22 ramas. El historial de `evidencias/historial_git.txt` y los reportes junit/coverage versionados deben interpretarse según el commit y timestamp que contienen, no como salida de este corte: el archivo de historial guardado termina en `c9114b5` y los reportes guardados son de una ejecución de 63 casos/99 sentencias/20 ramas.
- El texto “esta sesión no dispone de checkout local” de la sección 6 documenta la limitación existente durante la Fase 6, no el estado remoto ni una afirmación sobre el entorno actual.
