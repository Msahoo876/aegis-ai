"""
Security Utilities

Provides password hashing, password verification,
JWT creation, JWT decoding, and OAuth2 authentication
utilities for Aegis AI.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer

# ==========================================================
# Password Hashing
# ==========================================================

password_hasher = PasswordHash.recommended()

# ==========================================================
# OAuth2
# ==========================================================

# This will be used by FastAPI dependency injection later.

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)

# ==========================================================
# Password Utilities
# ==========================================================


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.
    """

    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against its hash.
    """

    return password_hasher.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# JWT Utilities
# ==========================================================


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    additional_claims: dict[str, Any] | None = None,
) -> str:
    """
    Create a signed JWT access token.
    """

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

    expire = datetime.now(UTC) + expires_delta

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
    }

    if additional_claims:
        payload.update(additional_claims)

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def get_token_subject(
    token: str,
) -> str:
    """
    Extract the user ID (subject) from a JWT.
    """

    payload = decode_access_token(token)

    subject = payload.get("sub")

    if subject is None:
        raise ValueError(
            "Invalid authentication token."
        )

    return subject

def decode_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return payload

    except JWTError as exc:
        raise ValueError("Invalid authentication token.") from exc