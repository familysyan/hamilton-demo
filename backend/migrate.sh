#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"
MIGRATIONS_DIR="${SCRIPT_DIR}/migrations"

usage() {
  echo "Usage: ./migrate.sh <up|down> <migration_folder>"
  echo "Example: ./migrate.sh up 0001_create_users_table"
}

if [[ $# -ne 2 ]]; then
  usage
  exit 1
fi

ACTION="$1"
MIGRATION_NAME="$2"

if [[ "${ACTION}" != "up" && "${ACTION}" != "down" ]]; then
  echo "Error: action must be 'up' or 'down'."
  usage
  exit 1
fi

SQL_FILE="${MIGRATIONS_DIR}/${MIGRATION_NAME}/${ACTION}.sql"

if [[ ! -f "${SQL_FILE}" ]]; then
  echo "Error: migration script not found: ${SQL_FILE}"
  exit 1
fi

echo "Starting PostgreSQL container if needed..."
docker compose -f "${COMPOSE_FILE}" up -d postgres >/dev/null

echo "Applying ${ACTION} for migration '${MIGRATION_NAME}'..."
docker compose -f "${COMPOSE_FILE}" exec -T postgres \
  psql -U hamilton -d hamilton -v ON_ERROR_STOP=1 -f - < "${SQL_FILE}"

echo "Done."
