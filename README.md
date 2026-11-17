# Orders API — Desafío técnico

## Contexto

Mantienes la API interna de pedidos de la empresa (FastAPI + SQLite). Soporte acumuló varios reportes y producto pidió un cambio pequeño en el listado.

No se espera que termines todo. Valoramos más **cómo** llegas a una conclusión —qué verificas, qué descartas y por qué— que la cantidad de cambios.

## Antes de la entrevista (≈10 min)

Sigue [`local/README.md`](local/README.md) y confirma que todo funciona:

```bash
uv run python scripts/check_env.py   # o: python scripts/check_env.py dentro de tu venv
```

Si el chequeo no queda en verde, avísanos antes de la sesión. Los problemas de instalación **no** se evalúan.

## Durante la entrevista (30–40 min)

| Tiempo | Qué hacer |
|--------|-----------|
| ~5 min | Contexto y preguntas iniciales |
| ~20–25 min | Resolver los reportes de soporte y el cambio de producto |
| ~10 min | Recorrer tus cambios con quien te entrevista: decisiones, riesgos y qué harías después |

**Usa IA como lo harías en tu trabajo diario** (Copilot, Cursor, Claude Code, ChatGPT, la que prefieras). Comparte pantalla completa, incluidos tus prompts. Evaluamos cómo la diriges y cómo verificas lo que propone.

Piensa en voz alta. Puedes hacer preguntas en cualquier momento: aclarar requisitos es parte del trabajo.

### 1. Reportes de soporte

1. **"El filtro por estado no hace nada."** `GET /orders?status=paid` devuelve pedidos con cualquier estado.
2. **"Pedidos grandes mal calculados."** `GET /orders/large?min_amount=500` muestra un pedido de $8.75 y no muestra el de $1.500.
3. **"Error 500 en estadísticas."** Abrir las estadísticas de `hooli`, un cliente nuevo, rompe la pantalla.
4. **"Etiquetas raras en el detalle."** A veces `GET /orders/{id}` muestra etiquetas que no corresponden al pedido. Soporte no logra reproducirlo siempre.

Para cada reporte: reprodúcelo, encuentra la causa, corrígela y, si alcanzas, deja un test que lo cubra.

### 2. Cambio de producto: listado paginado

Extender `GET /orders`:

- `status` (opcional): filtra por estado.
- `limit` (opcional, entero entre 1 y 100, por defecto 50).
- `offset` (opcional, entero ≥ 0, por defecto 0).
- Los tres se pueden combinar: `GET /orders?status=paid&limit=2&offset=2`.
- Orden: `created_at` descendente; a igual fecha, `id` descendente.
- Parámetros inválidos → `422`.
- **Compatibilidad:** la respuesta sigue siendo una **lista JSON** de pedidos, como hoy (ver [`docs/API.md`](docs/API.md)). Hay clientes que dependen de ese formato.

Agrega al menos un test.

## Entrega

Tu entrega son **Pull Requests contra este repositorio** (haz un fork y abre los PRs hacia `main`).

- Un cambio lógico por PR.
- Solo lo que pide este README. Lo demás que veas, anótalo en la descripción del PR; no lo implementes.
- En la descripción: qué resuelve, por qué ocurría y cómo lo verificaste. Si un PR depende de otro, indícalo.

## Comandos útiles

```bash
uv run uvicorn app.main:app --reload     # API en http://localhost:8000 (docs en /docs)
uv run pytest                            # tests
uv run python -m app.seed --reset        # recrear la base local
```

Otras formas de levantar el proyecto (venv + pip, Docker/Podman, Codespaces): [`local/README.md`](local/README.md).
