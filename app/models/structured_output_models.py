from pydantic import BaseModel
from app.models.workflow import WorkflowType


# ==========================================
# CLASSIFIER
# ==========================================

class WorkflowClassification(BaseModel):
    workflow_type: WorkflowType


# ==========================================
# OFFER LETTER
# ==========================================

class OfferLetterFields(BaseModel):
    employer: str
    ctc: float

    joining_date: str | None = None
    notice_period: int | None = None
    remote_policy: str | None = None


class OfferAnalysis(BaseModel):
    red_flags: list[str]
    negotiation_tips: list[str]

    requires_hitl: bool


# ==========================================
# SALARY SLIP
# ==========================================

class SalarySlipFields(BaseModel):
    gross_salary: float

    in_hand_salary: float

    pf_deduction: float | None = None

    tds_deduction: float | None = None

    employer_name: str

    pay_period: str




# ==========================================
# RECURRING BILL
# ==========================================

class RecurringBillExtraction(BaseModel):
    bill_name: str

    amount: float

    due_day: int

    frequency: str