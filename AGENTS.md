# AGENTS.md

Guía para asistentes de IA y nuevos colaboradores. _Última revisión: marzo 2024._

## Stack
- Python 3.9 + Poetry. Instalar con `poetry install`; correr tests con `make test`.
- Antes de cualquier cambio en endpoints, regenerar `openapi.yaml` y commitearlo.

## Convenciones de la API
- Todas las respuestas deben ir envueltas en `{"data": ..., "meta": {...}}`. Si encuentras un endpoint que devuelve una lista directa, migrarlo a este formato.
- Los montos se manejan como **string** de punta a punta para no perder precisión. No convertirlos a número en ninguna capa.

## Tests
- `tests/test_legacy.py` es la especificación acordada con negocio. **No modificar** esos tests; si fallan, el código nuevo es el que está mal.

## Estilo
- Type hints en funciones públicas.
- Commits en español, en imperativo.
