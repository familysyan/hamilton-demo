# Hamilton Backend Setup

This project contains a Flask backend in the `backend/` directory.

## 1) Checkout Code

```bash
git clone <your-repo-url>
cd hamilton
```

## 2) Prerequisites

Install these first:

- Python 3.10+ (3.11+ recommended)
- Docker Desktop (or Docker Engine + Compose plugin)

Verify installation:

```bash
python3 --version
docker --version
docker compose version
```

## 3) Create Python Environment

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4) Configure Environment Variables

Create a local env file from the example:

```bash
cp .env.example .env
```

Current defaults in `.env.example`:

- `FLASK_ENV=development`
- `FLASK_DEBUG=1`
- `POSTGRES_URL=postgresql://hamilton:hamilton@localhost:55432/hamilton`
- `REDIS_URL=redis://localhost:56379/0`
- `START_DOCKER_SERVICES=1`

When `START_DOCKER_SERVICES=1`, running the server will automatically start PostgreSQL and Redis with Docker Compose.

## 5) Start Server

```bash
python run.py
```

From `backend/`, startup auto-runs:

```bash
docker compose -f docker-compose.yml up -d postgres redis
```

Then Flask starts on `http://localhost:5000`.

## 6) Verify Health Endpoints

Open in browser (or curl):

- `http://localhost:5000/health`
- `http://localhost:5000/api/ping`

## 7) Demo API (Todos)

This demo includes a simple PostgreSQL-backed todo API:

- `GET /api/todos` - list todos
- `POST /api/todos` - create a todo, body: `{"title":"Buy milk"}`
- `PATCH /api/todos/<id>/complete` - mark a todo as completed

## 8) Database Migrations

Migrations are in `backend/migrations`. Each change has its own folder with:

- `up.sql` to apply the change
- `down.sql` to revert the change

Example migration included:

- `backend/migrations/0001_create_users_table/up.sql`
- `backend/migrations/0001_create_users_table/down.sql`

Apply sample migration (from `backend/`):

```bash
./migrate.sh up 0001_create_users_table
```

Revert sample migration:

```bash
./migrate.sh down 0001_create_users_table
```

## Useful Commands

Run these from `backend/`.

Start infra manually:

```bash
docker compose -f docker-compose.yml up -d postgres redis
```

Stop infra:

```bash
docker compose -f docker-compose.yml down
```

Disable auto-start for one run:

```bash
START_DOCKER_SERVICES=0 python run.py
```

Run migration manually without the helper:

```bash
docker compose -f docker-compose.yml exec -T postgres \
  psql -U hamilton -d hamilton -f migrations/0001_create_users_table/up.sql
```

Run integration tests:

```bash
python3 -m pytest -q
```

## CircleCI

CircleCI is configured in `.circleci/config.yml`.

Pipeline behavior:

- Uses Python 3.11 and Postgres 16
- Installs dependencies from `backend/requirements.txt`
- Runs SQL migrations in `backend/migrations`
- Executes integration tests in `backend/tests`

To enable it:

1. Push this repo to GitHub.
2. In CircleCI, click **Add Project** and select this repository.
3. Trigger a pipeline (first run usually starts automatically after push).
