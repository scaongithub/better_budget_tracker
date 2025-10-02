from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from .. import crud
from ..auth import get_current_user
from ..database import get_session
from ..models import User
from ..schemas import (
    MonthlySummary,
    TransactionCreate,
    TransactionRead,
    YearlySummary,
)
from ..services import calculate_monthly_summary, calculate_yearly_summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/monthly", response_model=MonthlySummary)
def get_monthly_summary(
    year: Optional[int] = None,
    month: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> MonthlySummary:
    today = date.today()
    target_year = year or today.year
    target_month = month or today.month

    if not 1 <= target_month <= 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be between 1 and 12",
        )

    return calculate_monthly_summary(session, current_user.id, target_year, target_month)


@router.get("/yearly", response_model=YearlySummary)
def get_yearly_summary(
    year: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> YearlySummary:
    target_year = year or date.today().year
    return calculate_yearly_summary(session, current_user.id, target_year)


@router.post("/transactions", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def add_transaction(
    transaction_in: TransactionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TransactionRead:
    transaction = crud.create_transaction(session, current_user, transaction_in)
    return TransactionRead.from_orm(transaction)


@router.get("/transactions", response_model=List[TransactionRead])
def list_user_transactions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[TransactionRead]:
    transactions = crud.list_transactions(session, current_user)
    return [TransactionRead.from_orm(txn) for txn in transactions]
