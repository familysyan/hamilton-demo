from flask import current_app
import psycopg


def get_connection() -> psycopg.Connection:
    return psycopg.connect(current_app.config["POSTGRES_URL"], autocommit=True)
