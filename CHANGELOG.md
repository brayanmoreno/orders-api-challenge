# Changelog

## 1.4.1 — 2026-03-14

### Fixed
- El filtro `status` en `GET /orders` ahora se aplica correctamente (#212).
- Mensaje de error más claro cuando el cliente no existe en `/customers/{slug}/stats`.

## 1.4.0 — 2026-03-01

### Added
- Endpoint `GET /customers/{slug}/stats`.
- Etiqueta `high-value` en el detalle de pedido.

### Fixed
- El detalle de pedido ya no comparte etiquetas entre requests (#198).

## 1.3.0 — 2026-01-20

### Changed
- Migración de Postgres a SQLite para simplificar el ambiente local.
- Se elimina la caché de Redis (no se usaba en la práctica).
