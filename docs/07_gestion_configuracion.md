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
- `refactor/estrategia` retiene su historial posterior a pruebas y su separación del código heredado. Se integra a `main` mediante PR revisado después de la suite.
- No se empleó force push ni se borraron ramas o commits.

### Ramas fix/DEF

No había evidencia de ramas `fix/DEF-01`, `fix/DEF-02`, `fix/DEF-03` ni `fix/DEF-04`. La Fase 5 corrigió los cuatro defectos dentro de commits reales de `refactor/estrategia` junto con la arquitectura modular; no aisló cada corrección en una rama ni un commit por defecto. Para no falsear el historial, esta fase no crea ramas vacías ni reconstruye commits artificiales. La trazabilidad se conserva mediante el mapeo DEF → casos BB en `docs/06_refactorizacion.md`, el historial original y la rama refactorizada. Si el curso requiere estrictamente ramas separadas, deberán desarrollarse como trabajo nuevo desde una base acordada, con cambios reales y PRs nuevos; no se pueden presentar como historial de Fase 5.

## 3. Etiquetas y releases

La etiqueta solicitada `v1.0.0` debe ser anotada y apuntar exactamente a `8fdc6625efaffb39dcb70d57c9495503fc096306`, nunca a la refactorización. La herramienta GitHub disponible en esta sesión permite ramas, archivos y merges, pero no expone creación de etiquetas ni refs de Git. La interfaz de Codespaces tampoco pudo abrirse mediante la automatización disponible. Por esa limitación no se afirma que la etiqueta haya sido creada. Créala y verifica su destino con:

```bash
git fetch origin --tags
git tag -a v1.0.0 8fdc6625efaffb39dcb70d57c9495503fc096306 -m "Release 1.0.0: implementación heredada"
git push origin v1.0.0
git show --no-patch --format="%H %D" v1.0.0
```

La última línea debe mostrar el SHA completo `8fdc6625efaffb39dcb70d57c9495503fc096306`. No se debe mover la etiqueta a un commit de refactorización.

## 4. Versionamiento semántico

La referencia heredada es `envios.calc(p, z, c, d, cup=None, flag=False)`; la nueva función es `src.calculadora.calc(peso, zona, cliente, dia, cup=None)`. Los nombres de parámetros cambian, `flag` desaparece y la ruta de importación nueva es distinta.

La rama refactor conserva el módulo `envios` y su firma para caracterizar el comportamiento anterior; añade un módulo de calculadora separado en `src`. Por tanto, el cambio versionado aquí es una nueva entrada modular compatible por adición para los consumidores que sigan usando `envios.calc`. Se registra como **1.1.0** (mejora compatible), no como ruptura automática. Un consumidor que migre a `src.calculadora.calc` sí debe ajustar su importación y dejar de pasar `flag`; esas instrucciones de migración se documentan en las notas de versión.

Si el proyecto declara en el futuro que `src.calculadora.calc` reemplaza oficialmente `envios.calc` y elimina el módulo/firma heredados, ese cambio contractual sí requiere un major (por ejemplo, 2.0.0). No se afirma que esa eliminación haya ocurrido en esta fase.

## 5. Historial y evidencia Git

Los commits observados son descriptivos y cronológicamente conservados. La topología comprobada por SHA y padres es: línea inicial `3ffcbe0 → 8fdc662 → 545ec59`; los 17 commits de Fases 1–4 concluyen en `37dd270); refactor/estrategia parte de `37dd270` y agrega sus commits Fase 5. La suite se integró a main mediante el merge `24dd667`, sin squash y preservando ambos padres. La salida completa local se obtiene con:

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

La salida SHA-1 esperada para ambos archivos es `5585b110170a271dadc20c11d67f8c62fb9a0b3c`. La ejecución documentada de 63 pruebas y cobertura está asociada al run 43109179938 sobre el commit de Fase 5; esta sesión no dispone de checkout local de Git/Python para repetir ese comando después de la integración. No se atribuye esa ejecución al commit final de main. La Fase 6 no implementa la zona insular.
