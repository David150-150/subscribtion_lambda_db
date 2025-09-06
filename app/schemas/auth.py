from pydantic import BaseModel, EmailStr

# Input credentials for login
class LoginInput(BaseModel):
    email: EmailStr
    password: str

# Response with token after login
class Token(BaseModel):
    access_token: str
    token_type: str
