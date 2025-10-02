from __future__ import annotations

from datetime import date

from sqlmodel import Session, select

from .models import Recurrence, Transaction, TransactionType, User
from .security import hash_password


def _get_or_create_user(
    session: Session,
    username: str,
    full_name: str,
    password: str,
    monthly_budget_goal: float,
) -> User:
    user = session.exec(select(User).where(User.username == username)).first()
    if user:
        return user

    user = User(
        username=username,
        full_name=full_name,
        hashed_password=hash_password(password),
        monthly_budget_goal=monthly_budget_goal,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def seed_initial_data(session: Session) -> None:
    carlo = _get_or_create_user(
        session,
        username="carlo",
        full_name="Carlo Bianchi",
        password="carlo123",
        monthly_budget_goal=2800.0,
    )
    paola = _get_or_create_user(
        session,
        username="paola",
        full_name="Paola Verdi",
        password="paola123",
        monthly_budget_goal=3200.0,
    )

    if not session.exec(select(Transaction).where(Transaction.user_id == carlo.id)).first():
        session.add_all(
            [
                Transaction(
                    user_id=carlo.id,
                    amount=3200.0,
                    description="Monthly salary",
                    date=date(2024, 1, 1),
                    type=TransactionType.income,
                    recurrence=Recurrence.monthly,
                ),
                Transaction(
                    user_id=carlo.id,
                    amount=900.0,
                    description="Rent",
                    date=date(2024, 1, 5),
                    type=TransactionType.expense,
                    recurrence=Recurrence.monthly,
                ),
                Transaction(
                    user_id=carlo.id,
                    amount=120.0,
                    description="Gym membership",
                    date=date(2024, 1, 10),
                    type=TransactionType.expense,
                    recurrence=Recurrence.monthly,
                ),
                Transaction(
                    user_id=carlo.id,
                    amount=200.0,
                    description="Freelance project",
                    date=date(2024, 3, 18),
                    type=TransactionType.income,
                    recurrence=Recurrence.none,
                ),
            ]
        )

    if not session.exec(select(Transaction).where(Transaction.user_id == paola.id)).first():
        session.add_all(
            [
                Transaction(
                    user_id=paola.id,
                    amount=3500.0,
                    description="Primary salary",
                    date=date(2024, 1, 1),
                    type=TransactionType.income,
                    recurrence=Recurrence.monthly,
                ),
                Transaction(
                    user_id=paola.id,
                    amount=150.0,
                    description="Yoga classes",
                    date=date(2024, 1, 12),
                    type=TransactionType.expense,
                    recurrence=Recurrence.monthly,
                ),
                Transaction(
                    user_id=paola.id,
                    amount=600.0,
                    description="Mortgage",
                    date=date(2024, 1, 3),
                    type=TransactionType.expense,
                    recurrence=Recurrence.monthly,
                ),
                Transaction(
                    user_id=paola.id,
                    amount=450.0,
                    description="Yearly insurance",
                    date=date(2024, 2, 15),
                    type=TransactionType.expense,
                    recurrence=Recurrence.yearly,
                ),
            ]
        )

    session.commit()
