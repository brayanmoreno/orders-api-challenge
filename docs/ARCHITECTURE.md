# Arquitectura

_Última revisión: noviembre 2025._

```
cliente ──► FastAPI ──► Redis (caché de listados, TTL 60 s)
                    └─► Postgres 14 (fuente de verdad)
```

- **Postgres 14** es la base de datos. Las migraciones se manejan con **Alembic** (`alembic upgrade head`).
- **Redis** cachea `GET /orders` por 60 segundos. Si ves datos "viejos" o un filtro que no responde, lo más probable es la caché: ejecuta `redis-cli FLUSHALL`.
- Los montos se almacenan como `NUMERIC(12,2)`.
- La capa `repository` concentra todo el SQL; `services` contiene reglas de negocio puras.
