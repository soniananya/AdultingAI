from pydantic import BaseModel
from datetime import datetime
from typing import Any


class RecurringBill(BaseModel):
    name: str
    amount: float
    due_day: int
    frequency: str


class LifeState(BaseModel):
    current_salary: float | None = None
    employer: str | None = None
    monthly_rent: float | None = None

    pan_number: str | None = None
    tax_regime: str | None = None

    recurring_bills: list[RecurringBill] = []

    profile: dict[str, Any] = {}

    last_updated: datetime | None = None


class LifeStateUpdate(BaseModel):
    current_salary: float | None = None
    employer: str | None = None
    monthly_rent: float | None = None

    pan_number: str | None = None
    tax_regime: str | None = None

    recurring_bills: list[RecurringBill] | None = None

    profile: dict[str, Any] | None = None