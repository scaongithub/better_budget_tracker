from __future__ import annotations

from fastapi import APIRouter, Depends

from ..auth import login
from ..schemas import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    token: Token = Depends(login),
) -> Token:
    return token
