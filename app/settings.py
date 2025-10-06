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

# import os

# from dotenv import load_dotenv

# load_dotenv()  # Load .env variables

# class Settings:
#     TESTING: bool = os.getenv("TESTING", "0") == "1"
#     IN_DOCKER: bool = os.getenv("IN_DOCKER", "0") == "1"

#     if TESTING:
#         DATABASE_URL = os.getenv("TEST_DATABASE_URL")
#     elif IN_DOCKER:
#         DATABASE_URL = (
#             f"mysql+mysqlconnector://{os.getenv('DOCKER_DB_USER')}:{os.getenv('DOCKER_DB_PASSWORD')}" f"@{os.getenv('DOCKER_DB_HOST')}:{os.getenv('DOCKER_DB_PORT')}/{os.getenv('DOCKER_DB_NAME')}"
#         )
#     else:
#         DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}" f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


# settings = Settings()


# import os

# from dotenv import load_dotenv

# load_dotenv()  # Load .env variables


# class Settings:
#     TESTING: bool = os.getenv("TESTING", "0") == "1"
#     IN_DOCKER: bool = os.getenv("IN_DOCKER", "0") == "1"

#     if TESTING:
#         DATABASE_URL = os.getenv("TEST_DATABASE_URL")
#     elif IN_DOCKER:
#         DATABASE_URL = (
#             f"mysql+mysqlconnector://{os.getenv('DOCKER_DB_USER')}:{os.getenv('DOCKER_DB_PASSWORD')}" f"@{os.getenv('DOCKER_DB_HOST')}:{os.getenv('DOCKER_DB_PORT')}/{os.getenv('DOCKER_DB_NAME')}"
#         )
#     else:
#         DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}" f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


# settings = Settings()


# import os

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
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", f"mysql+mysqlconnector://{DOCKER_DB_USER}:{DOCKER_DB_PASSWORD}@mysql:3306/{DOCKER_DB_NAME}")

# Decide which URL to use
if TESTING:
    DATABASE_URL = TEST_DATABASE_URL
elif IN_DOCKER:
    DATABASE_URL = f"mysql+mysqlconnector://{DOCKER_DB_USER}:{DOCKER_DB_PASSWORD}@{DOCKER_DB_HOST}:{DOCKER_DB_PORT}/{DOCKER_DB_NAME}"
else:
    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
