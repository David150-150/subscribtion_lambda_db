# app/settings.py
import os

from dotenv import load_dotenv

load_dotenv()  # Load .env variables


class Settings:
    # Mode switches
    IN_DOCKER = os.getenv("IN_DOCKER", "0") == "1"
    TESTING = os.getenv("TESTING", "0") == "1"

    # Local development
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "newpass123")
    DB_NAME = os.getenv("DB_NAME", "SubscribDB")

    # Docker Compose
    DOCKER_DB_HOST = os.getenv("DOCKER_DB_HOST", "db")
    DOCKER_DB_PORT = os.getenv("DOCKER_DB_PORT", "3306")
    DOCKER_DB_USER = os.getenv("DOCKER_DB_USER", "root")
    DOCKER_DB_PASSWORD = os.getenv("DOCKER_DB_PASSWORD", "newpass123")
    DOCKER_DB_NAME = os.getenv("DOCKER_DB_NAME", "test_SubscribDB")

    # Testing / CI
    TEST_DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL",
        f"mysql+mysqlconnector://{DOCKER_DB_USER}:{DOCKER_DB_PASSWORD}@127.0.0.1:3306/{DOCKER_DB_NAME}",
    )

    # Decide which URL to use
    if TESTING:
        DATABASE_URL = TEST_DATABASE_URL
    elif IN_DOCKER:
        DATABASE_URL = f"mysql+mysqlconnector://{DOCKER_DB_USER}:{DOCKER_DB_PASSWORD}@{DOCKER_DB_HOST}:{DOCKER_DB_PORT}/{DOCKER_DB_NAME}"
    else:
        DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


settings = Settings()
