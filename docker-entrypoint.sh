#!/bin/sh
set -eu

echo "Aplicando migrações do banco..."

/app/.venv/bin/alembic upgrade head

echo "Migrações aplicadas."

exec "$@"