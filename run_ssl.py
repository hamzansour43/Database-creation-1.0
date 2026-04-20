"""WSGI wrapper for running Flask with SSL using gunicorn."""
import os
import subprocess
import sys

from app import app


if __name__ == "__main__":
    port = os.getenv("HTTPS_PORT", "5000")
    workers = os.getenv("GUNICORN_WORKERS", "4")
    timeout = os.getenv("GUNICORN_TIMEOUT", "15")

    sys.exit(subprocess.call([
        sys.executable,
        "-m",
        "gunicorn",
        "--bind",
        f"0.0.0.0:{port}",
        "--certfile",
        "cert.pem",
        "--keyfile",
        "key.pem",
        "--workers",
        workers,
        "--worker-class",
        "sync",
        "--backlog",
        "256",
        "--timeout",
        timeout,
        "--graceful-timeout",
        "5",
        "--keep-alive",
        "2",
        "--access-logfile",
        "-",
        "--error-logfile",
        "-",
        "app:app",
    ]))