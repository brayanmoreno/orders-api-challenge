"""Verifica que el ambiente esté listo para la entrevista.

Uso:
    uv run python scripts/check_env.py
    python scripts/check_env.py          # dentro de tu venv

No usa red ni toca nada fuera del repositorio (salvo crear data/orders.db).
"""

from __future__ import annotations

import importlib
import os
import shutil
import socket
import subprocess
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", message="Using `httpx`")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OK, FAIL = "\033[32m✔\033[0m", "\033[31m✘\033[0m"
problems: list[str] = []


def check(label: str, ok: bool, hint: str = "") -> None:
    print(f"  {OK if ok else FAIL} {label}")
    if not ok:
        problems.append(f"{label}: {hint}" if hint else label)


print("Chequeando ambiente…\n")

check(
    f"Python {sys.version.split()[0]} (>= 3.12)",
    sys.version_info >= (3, 12),
    "instala Python 3.12+ o usa `uv run`, que lo descarga solo",
)

for module in ("fastapi", "uvicorn", "pytest", "httpx"):
    try:
        importlib.import_module(module)
        check(f"Dependencia {module}", True)
    except ImportError:
        check(f"Dependencia {module}", False, "ejecuta `uv sync` o `pip install -r requirements.txt -r requirements-dev.txt`")

try:
    from app.seed import init_db
    from app.db import get_db_path

    init_db()
    check(f"Base SQLite en {get_db_path().relative_to(ROOT) if get_db_path().is_relative_to(ROOT) else get_db_path()}", True)
except Exception as exc:  # noqa: BLE001
    check("Base SQLite", False, repr(exc))

port = int(os.environ.get("PORT", "8000"))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    free = s.connect_ex(("127.0.0.1", port)) != 0
check(f"Puerto {port} libre", free, "cierra lo que lo usa o define PORT=8001")

try:
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as client:
        check("La API responde /health", client.get("/health").status_code == 200)
except Exception as exc:  # noqa: BLE001
    check("La API responde /health", False, repr(exc))

# Avisos no bloqueantes: git/gh solo se usan para entregar.
WARN = "\033[33m!\033[0m"


def _version(cmd: list[str]) -> str | None:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


git = _version(["git", "--version"]) if shutil.which("git") else None
print(f"  {OK if git else WARN} git: {git or 'no encontrado (lo necesitarás para entregar)'}")
if shutil.which("gh"):
    authed = subprocess.run(["gh", "auth", "status"], capture_output=True).returncode == 0
    print(f"  {OK if authed else WARN} GitHub CLI: {'autenticado' if authed else 'instalado, sin login (`gh auth login`)'}")
else:
    print(f"  {WARN} GitHub CLI no instalado (opcional: también puedes abrir PRs desde la web)")

print()
if problems:
    print("Hay problemas que resolver antes de la entrevista:")
    for p in problems:
        print(f"  - {p}")
    sys.exit(1)
print(f"{OK} Todo listo. Nos vemos en la entrevista.")
print("  (Es normal que algunos tests fallen: son parte del desafío.)")
