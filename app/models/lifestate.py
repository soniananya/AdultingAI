from pydantic import BaseModel
from typing import Any


class RecurringBill(BaseModel):

    name: str

    amount: float

    due_day: int

    frequency: str


class LifeStateSnapshot(BaseModel):

    current_salary: float | None = None

    employer: str | None = None

    monthly_rent: float | None = None

    current_city: str | None = None

    housing_type: str | None = None

    employment_type: str | None = None

    joining_date: str | None = None

    recurring_bills: list[RecurringBill] = []

    resume_url: str | None = None

    skills: list[str] = []

    pan_number: str | None = None

    tax_regime: str | None = None


class LifeStateUpdate(BaseModel):

    current_salary: float | None = None

    employer: str | None = None

    monthly_rent: float | None = None

    current_city: str | None = None

    housing_type: str | None = None

    employment_type: str | None = None

    joining_date: str | None = None

    resume_url: str | None = None

    skills: list[str] | None = None

    pan_number: str | None = None

    tax_regime: str | None = None

    recurring_bills: list[RecurringBill] | None = None


# Alias: the lifestate router refers to the profile model as `LifeState`.
LifeState = LifeStateSnapshot