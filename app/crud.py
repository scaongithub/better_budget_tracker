from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlmodel import Session, select

from .models import Transaction, User
from .schemas import TransactionCreate


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def create_transaction(session: Session, user: User, transaction_in: TransactionCreate) -> Transaction:
    transaction = Transaction(
        user_id=user.id,
        amount=transaction_in.amount,
        description=transaction_in.description or "",
        date=transaction_in.date,
        type=transaction_in.type,
        recurrence=transaction_in.recurrence,
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def list_transactions(session: Session, user: User) -> List[Transaction]:
    statement = select(Transaction).where(Transaction.user_id == user.id).order_by(Transaction.date)
    return list(session.exec(statement))


def transactions_for_timeframe(
    session: Session,
    user: User,
    start_date: date,
    end_date: date,
) -> List[Transaction]:
    statement = (
        select(Transaction)
        .where(Transaction.user_id == user.id)
        .where(Transaction.date.between(start_date, end_date))
        .order_by(Transaction.date)
    )
    return list(session.exec(statement))
