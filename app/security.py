from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple


def hash_password(password: str, salt: Optional[str] = None) -> str:
    if salt is None:
        salt_bytes = secrets.token_bytes(16)
    else:
        salt_bytes = bytes.fromhex(salt)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, 390000)
    return f"{salt_bytes.hex()}:{dk.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        salt_hex, hash_hex = hashed_password.split(":", 1)
    except ValueError:
        return False
    recalculated = hash_password(password, salt_hex)
    return hmac.compare_digest(recalculated, hashed_password)


class TokenStore:
    def __init__(self) -> None:
        self._tokens: Dict[str, Tuple[int, datetime]] = {}

    def create_token(self, user_id: int, expires_delta: timedelta) -> str:
        token = secrets.token_urlsafe(32)
        self._tokens[token] = (user_id, datetime.utcnow() + expires_delta)
        return token

    def get_user_id(self, token: str) -> Optional[int]:
        data = self._tokens.get(token)
        if not data:
            return None
        user_id, expires = data
        if datetime.utcnow() >= expires:
            self._tokens.pop(token, None)
            return None
        return user_id

    def revoke(self, token: str) -> None:
        self._tokens.pop(token, None)


ACCESS_TOKEN_EXPIRE_MINUTES = 60
