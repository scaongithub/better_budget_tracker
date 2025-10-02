from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from .models import Recurrence, TransactionType


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class UserRead(BaseModel):
    id: int
    username: str
    full_name: str
    monthly_budget_goal: Optional[float] = None

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    amount: float = Field(gt=0)
    description: Optional[str] = Field(default="", max_length=255)
    date: date
    type: TransactionType
    recurrence: Recurrence = Recurrence.none


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int

    class Config:
        orm_mode = True


class MonthlySummary(BaseModel):
    month: int
    year: int
    income_total: float
    expense_total: float
    net_total: float
    transactions: List[TransactionRead]


class MonthlyBreakdown(BaseModel):
    month: int
    income_total: float
    expense_total: float
    net_total: float


class YearlySummary(BaseModel):
    year: int
    monthly_breakdown: List[MonthlyBreakdown]
    yearly_income_total: float
    yearly_expense_total: float
    yearly_net_total: float
