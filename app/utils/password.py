# # app/utils/password.py
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def hash_password(password: str) -> str:
#     """
#     Hash the password safely using bcrypt.
#     Truncate password to 72 characters to avoid bcrypt limit.
#     """
#     safe_password = password[:72]  # bcrypt max is 72 bytes
#     return pwd_context.hash(safe_password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     safe_password = plain_password[:72]  # also truncate when verifying
#     return pwd_context.verify(safe_password, hashed_password)


# # app/utils/password.py
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# MAX_BCRYPT_LENGTH = 72  # bcrypt limit in bytes


# def hash_password(password: str) -> str:
#     """
#     Hash the password safely using bcrypt.
#     Truncate password to 72 characters to avoid bcrypt limit.
#     """
#     if len(password) > MAX_BCRYPT_LENGTH:
#         # Optional: log a warning that password is truncated
#         print(f"Warning: password truncated to {MAX_BCRYPT_LENGTH} characters for bcrypt")
#     safe_password = password[:MAX_BCRYPT_LENGTH]
#     return pwd_context.hash(safe_password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     Verify the password against the hashed version.
#     Truncate plain password to 72 characters to match bcrypt limit.
#     """
#     safe_password = plain_password[:MAX_BCRYPT_LENGTH]
#     return pwd_context.verify(safe_password, hashed_password)


# app/utils/password.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# put this first
def safe_password(pwd: str) -> str:
    return pwd.encode("utf-8")[:72].decode("utf-8", "ignore")


def hash_password(password: str) -> str:
    safe_pwd = safe_password(password)  # always truncate
    return pwd_context.hash(safe_pwd)
