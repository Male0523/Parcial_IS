# Changelog

All notable changes to EnvíaYa are documented here, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project uses Semantic Versioning for named releases.

## [Unreleased]

### Added
- Configuration management record for branch, tag, integration, and release history.

## [1.1.0] - 2026-11-11

### Added
- Modular calculator under `src/`, zone strategies, and regression checks.
- Automated suite with 41 functional cases (BB-01–BB-41), 15 structural paths (P01–P15), and 7 additional defensive regressions.

### Changed
- Added the independent public entry point `src.calculadora.calc(peso, zona, cliente, dia, cup=None)`.
- Retained `envios.calc(p, z, c, d, cup=None, flag=False)` unchanged as the historical implementation and structural test target.

### Fixed
- DEF-01: 3 kg now belongs to the second tariff tier.
- DEF-02: invalid zone and day inputs are rejected.
- DEF-03: Saturday and Sunday receive the weekend surcharge before discounts.
- DEF-04: amounts round to the nearest $100, with $50 ties rounded upward.

### Quality
- GitHub Actions run 43109179938: 63 tests passed, 0 failed, 0 errors.
- Coverage for active `src/`: 99/99 statements and 20/20 branches (100%); legacy Fase 4 baseline was measured separately and preserved in `docs/05_resultados_pruebas.md`.
- No island zone was implemented.

### Compatibility
- The new function is in a different module and has a different signature. Existing imports of `envios.calc` remain available. Migration to `src.calculadora.calc` requires changing the import and removing the former `flag` argument; see `docs/releases/v1.1.0.md`.

## [1.0.0] - 2026-11-11

### Added
- Original inherited implementation and custom parameters, preserved at commit `8fdc6625efaffb39dcb70d57c9495503fc096306`.
- Black-box requirements and test design documentation began after this baseline.

### Compatibility
- Public legacy function: `envios.calc(p, z, c, d, cup=None, flag=False)`.
- This release is the unmodified inherited snapshot. The `v1.0.0` tag must resolve to the original commit, not a later documentation or refactor commit.

[Unreleased]: https://github.com/Male0523/Parcial_IS/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/Male0523/Parcial_IS/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Male0523/Parcial_IS/tree/v1.0.0
