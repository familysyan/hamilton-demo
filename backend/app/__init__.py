import os

from flask import Flask

from .routes import api


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["ENV"] = os.getenv("FLASK_ENV", "development")
    app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "1") == "1"
    app.config["POSTGRES_URL"] = os.getenv(
        "POSTGRES_URL",
        "postgresql://hamilton:hamilton@localhost:55432/hamilton",
    )
    app.config["REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:56379/0")

    app.register_blueprint(api)
    return app
