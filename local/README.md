# Ambiente local

Tres formas de levantar el proyecto. Elige **una**; la recomendada es `uv`.
Todas sirven en macOS, Linux y Windows (con WSL2).

Al terminar, corre el chequeo:

```bash
uv run python scripts/check_env.py      # o: python scripts/check_env.py
```

Debe terminar con `✔ Todo listo`. **Es normal que algunos tests fallen**: son parte del desafío.

---

## Opción 1 — `uv` (recomendada)

[`uv`](https://docs.astral.sh/uv/) descarga Python 3.12 si no lo tienes. No necesitas instalar Python a mano.

```bash
# Instalar uv (una vez)
curl -LsSf https://astral.sh/uv/install.sh | sh       # macOS / Linux / WSL
# o: brew install uv  |  pipx install uv

# Desde la raíz del repo
uv sync
uv run uvicorn app.main:app --reload    # http://localhost:8000/docs
uv run pytest
```

## Opción 2 — `venv` + `pip`

Requiere Python **3.12 o superior** (`python3 --version`).

```bash
python3 -m venv .venv
source .venv/bin/activate              # Windows sin WSL: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
pytest
```

## Opción 3 — Contenedor (Docker Desktop, Colima, Podman, Rancher…)

No depende de ningún runtime en particular: sirve cualquiera compatible con `compose`.

```bash
cp local/conf/app.env.example local/conf/app.env   # opcional: cambiar PORT
docker compose -f local/docker-compose.yml up --build
# Podman:  podman compose -f local/docker-compose.yml up --build

# Tests dentro del contenedor
docker compose -f local/docker-compose.yml run --rm api pytest
```

El código se monta desde tu disco, así que los cambios se recargan solos. La base SQLite vive en un volumen del contenedor (`orders_data`); para recrearla:

```bash
docker compose -f local/docker-compose.yml down -v
```

> **Colima:** `colima start` antes de usar `docker`.
> **Podman en macOS:** `podman machine init && podman machine start` la primera vez.
> **Apple Silicon:** la imagen base `python:3.12-slim` es multi-arquitectura; no hace falta `--platform`.

## Opción 4 — Plan C: GitHub Codespaces

Si nada de lo anterior funciona en tu equipo: botón **Code → Codespaces → Create codespace** en GitHub. El `.devcontainer/` instala todo solo; luego `uvicorn app.main:app --reload --host 0.0.0.0`.

## `just` (opcional)

Si usas [`just`](https://github.com/casey/just), `local/justfile` tiene atajos (`just -f local/justfile --list`). No es requisito: cada receta es uno de los comandos de arriba.

## Problemas frecuentes

| Síntoma | Solución |
|---|---|
| `Address already in use` | Otro proceso usa el 8000: `uvicorn app.main:app --port 8001` o `PORT=8001` en `local/conf/app.env` |
| `ModuleNotFoundError: app` | Ejecuta los comandos desde la **raíz** del repo, no desde `local/` |
| Python 3.11 o menor | Usa la opción 1 (`uv` trae su propio Python) |
| Windows: errores raros de fin de línea | Clona dentro de WSL (`~/…`), no en `/mnt/c/…` |
| Datos "raros" tras experimentar | `uv run python -m app.seed --reset` |
