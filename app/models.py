from __future__ import annotations

import enum
from datetime import date
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Recurrence(str, enum.Enum):
    none = "none"
    monthly = "monthly"
    yearly = "yearly"


class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    full_name: str
    hashed_password: str
    monthly_budget_goal: Optional[float] = Field(default=None)

    transactions: List["Transaction"] = Relationship(back_populates="user")


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    amount: float
    description: str = Field(default="")
    date: date
    type: TransactionType
    recurrence: Recurrence = Field(default=Recurrence.none)

    user: Optional[User] = Relationship(back_populates="transactions")
