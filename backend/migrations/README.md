# Database Migrations

This folder stores raw SQL migrations for PostgreSQL.

## Structure

Each database change must live in its own subfolder:

```text
migrations/
  0001_change_name/
    up.sql
    down.sql
```

- `up.sql`: applies the change
- `down.sql`: reverts the same change

Use numeric prefixes in ascending order (`0001`, `0002`, ...) so migration order is clear.

## Running a Migration

Use the helper script (recommended) from `backend/`:

```bash
./migrate.sh up 0001_create_users_table
```

Equivalent direct command:

```bash
docker compose -f docker-compose.yml exec -T postgres \
  psql -U hamilton -d hamilton -f migrations/0001_create_users_table/up.sql
```

## Reverting a Migration

Use the helper script (recommended):

```bash
./migrate.sh down 0001_create_users_table
```

Equivalent direct command:

```bash
docker compose -f docker-compose.yml exec -T postgres \
  psql -U hamilton -d hamilton -f migrations/0001_create_users_table/down.sql
```
