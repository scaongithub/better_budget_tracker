from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date
from typing import List

from sqlmodel import Session, select

from .models import Recurrence, Transaction, TransactionType
from .schemas import MonthlyBreakdown, MonthlySummary, TransactionRead, YearlySummary


@dataclass
class MonthlyTotals:
    income: float = 0.0
    expenses: float = 0.0

    @property
    def net(self) -> float:
        return self.income - self.expenses


def _transaction_applies_to_month(transaction: Transaction, year: int, month: int) -> bool:
    _, last_day = calendar.monthrange(year, month)
    month_end = date(year, month, last_day)

    if transaction.recurrence == Recurrence.none:
        return transaction.date.year == year and transaction.date.month == month

    if transaction.recurrence == Recurrence.monthly:
        return transaction.date <= month_end

    if transaction.recurrence == Recurrence.yearly:
        return transaction.date.month == month and transaction.date <= month_end

    return False


def _load_user_transactions(session: Session, user_id: int) -> List[Transaction]:
    statement = select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.date)
    return list(session.exec(statement))


def calculate_monthly_summary(session: Session, user_id: int, year: int, month: int) -> MonthlySummary:
    transactions = _load_user_transactions(session, user_id)
    applicable_transactions = [
        txn for txn in transactions if _transaction_applies_to_month(txn, year, month)
    ]

    totals = MonthlyTotals()
    for txn in applicable_transactions:
        if txn.type == TransactionType.income:
            totals.income += txn.amount
        else:
            totals.expenses += txn.amount

    return MonthlySummary(
        month=month,
        year=year,
        income_total=round(totals.income, 2),
        expense_total=round(totals.expenses, 2),
        net_total=round(totals.net, 2),
        transactions=[TransactionRead.from_orm(txn) for txn in applicable_transactions],
    )


def calculate_yearly_summary(session: Session, user_id: int, year: int) -> YearlySummary:
    transactions = _load_user_transactions(session, user_id)

    monthly_breakdowns: List[MonthlyBreakdown] = []
    yearly_income = 0.0
    yearly_expense = 0.0

    for month in range(1, 13):
        applicable_transactions = [
            txn for txn in transactions if _transaction_applies_to_month(txn, year, month)
        ]
        totals = MonthlyTotals()
        for txn in applicable_transactions:
            if txn.type == TransactionType.income:
                totals.income += txn.amount
            else:
                totals.expenses += txn.amount

        monthly_breakdowns.append(
            MonthlyBreakdown(
                month=month,
                income_total=round(totals.income, 2),
                expense_total=round(totals.expenses, 2),
                net_total=round(totals.net, 2),
            )
        )
        yearly_income += totals.income
        yearly_expense += totals.expenses

    return YearlySummary(
        year=year,
        monthly_breakdown=monthly_breakdowns,
        yearly_income_total=round(yearly_income, 2),
        yearly_expense_total=round(yearly_expense, 2),
        yearly_net_total=round(yearly_income - yearly_expense, 2),
    )
