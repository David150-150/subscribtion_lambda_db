from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_handler import decode_access_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials and credentials.scheme == "Bearer":
            if self.verify_jwt(credentials.credentials):
                return credentials.credentials
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    def verify_jwt(self, token: str) -> bool:
        payload = decode_access_token(token)
        return payload is not None
