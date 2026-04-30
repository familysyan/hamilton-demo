# Project Setup Summary

This document summarizes the current backend infrastructure, database testing behavior, migration workflow, and CircleCI configuration.

## 1) Docker for Redis and Postgres

Infrastructure is defined in `backend/docker-compose.yml`:

- `postgres` (image: `postgres:16-alpine`)
- `redis` (image: `redis:7-alpine`)
- persistent named volumes for both services
- container health checks

Current local host ports:

- Postgres: `localhost:55432` -> container `5432`
- Redis: `localhost:56379` -> container `6379`

Start services manually:

```bash
cd backend
docker compose -f docker-compose.yml up -d postgres redis
```

Stop services:

```bash
cd backend
docker compose -f docker-compose.yml down
```

When running `python run.py`, backend startup also brings up `postgres` and `redis` automatically (unless `START_DOCKER_SERVICES=0`).

## 2) Auto DB Cleanup for Tests via Fixtures

Test DB cleanup is handled automatically in `backend/tests/conftest.py`.

How it works:

- a global `autouse=True` fixture runs for every test
- it truncates all tables in `public` schema
- it resets identities (`RESTART IDENTITY`) and cascades to dependent tables

Result: each test starts with a clean database state without adding cleanup code inside individual test files.

## 3) Auto Apply DB Migrations

Migrations live under `backend/migrations`, one folder per change:

```text
migrations/
  0001_create_users_table/
    up.sql
    down.sql
  0002_create_todos_table/
    up.sql
    down.sql
```

Migration helper script:

- `backend/migrate.sh up <migration_folder>`
- `backend/migrate.sh down <migration_folder>`

Example:

```bash
cd backend
./migrate.sh up 0001_create_users_table
./migrate.sh up 0002_create_todos_table
```

In CI, migrations are applied automatically before tests in `.circleci/config.yml`.

## 4) CircleCI Setup

Pipeline config file: `.circleci/config.yml`

Current CI job (`test`) does:

1. uses `cimg/python:3.11`
2. starts Postgres service (`cimg/postgres:16.3`)
3. installs Python deps from `backend/requirements.txt`
4. waits until Postgres is ready
5. runs SQL migrations (`0001` and `0002`)
6. runs integration tests: `cd backend && python -m pytest -q`

Recommended trigger configuration in CircleCI:

- `Pushes to open non-draft PRs` (runs on PR updates)
- optionally add `PR opened` if you also want a run immediately when a PR is first created
