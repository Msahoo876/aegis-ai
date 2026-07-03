"""
Authentication Schemas
"""

from pydantic import BaseModel


class Token(BaseModel):
    """
    JWT access token response.
    """

    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """
    User login request.
    """

    email: str
    password: str