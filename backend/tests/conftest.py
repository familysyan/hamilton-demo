import psycopg
import pytest
from psycopg import sql

from app import create_app


@pytest.fixture(scope="session")
def app():
    flask_app = create_app()
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


def _truncate_public_tables(postgres_url: str) -> None:
    with psycopg.connect(postgres_url, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
                """
            )
            table_names = [row[0] for row in cur.fetchall()]

            if not table_names:
                return

            identifiers = [sql.Identifier(table_name) for table_name in table_names]
            statement = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE").format(
                sql.SQL(", ").join(identifiers)
            )
            cur.execute(statement)


@pytest.fixture(autouse=True)
def clean_db(app):
    _truncate_public_tables(app.config["POSTGRES_URL"])
