import os
import subprocess
from pathlib import Path

from app import create_app


def start_infra_services() -> None:
    if os.getenv("START_DOCKER_SERVICES", "1") != "1":
        return

    compose_file = os.getenv(
        "DOCKER_COMPOSE_FILE",
        str(Path(__file__).resolve().parent / "docker-compose.yml"),
    )

    subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            compose_file,
            "up",
            "-d",
            "postgres",
            "redis",
        ],
        check=True,
    )

app = create_app()


if __name__ == "__main__":
    start_infra_services()
    app.run(host="0.0.0.0", port=5000)
