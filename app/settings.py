# app/settings.py
import os

from dotenv import load_dotenv

load_dotenv()  # Load .env variables


# class Settings:
#     # Switch to test database if TESTING=1
#     TESTING: bool = os.getenv("TESTING", "0") == "1"

#     DB_HOST: str = os.getenv("DB_HOST")
#     DB_PORT: str = os.getenv("DB_PORT")
#     DB_USER: str = os.getenv("DB_USER")
#     DB_PASSWORD: str = os.getenv("DB_PASSWORD")
#     DB_NAME: str = os.getenv("DB_NAME")

#     # Pick correct database URL
#     DATABASE_URL: str = os.getenv("TEST_DATABASE_URL") if TESTING else f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#     # Auth settings
#     SECRET_KEY: str = os.getenv("SECRET_KEY")
#     ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# settings = Settings()


class Settings:
    TESTING: bool = os.getenv("TESTING", "0") == "1"
    IN_DOCKER: bool = os.getenv("IN_DOCKER", "0") == "1"

    if TESTING:
        DATABASE_URL = os.getenv("TEST_DATABASE_URL")
    elif IN_DOCKER:
        DATABASE_URL = (
            f"mysql+mysqlconnector://{os.getenv('DOCKER_DB_USER')}:{os.getenv('DOCKER_DB_PASSWORD')}" f"@{os.getenv('DOCKER_DB_HOST')}:{os.getenv('DOCKER_DB_PORT')}/{os.getenv('DOCKER_DB_NAME')}"
        )
    else:
        DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}" f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
