# app/utils/password.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash the password safely using bcrypt.
    Truncate password to 72 characters to avoid bcrypt limit.
    """
    safe_password = password[:72]  # bcrypt max is 72 bytes
    return pwd_context.hash(safe_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    safe_password = plain_password[:72]  # also truncate when verifying
    return pwd_context.verify(safe_password, hashed_password)
