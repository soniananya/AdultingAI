from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Any
from uuid import UUID


class WorkflowStatus(Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class WorkflowType(Enum):
    SALARY_SLIP = "SALARY_SLIP"
    OFFER_LETTER = "OFFER_LETTER"
    RECURRING_BILL = "RECURRING_BILL"
    JD_ANALYSIS="JD_ANALYSIS"


class WorkflowCreate(BaseModel):
    user_id: UUID
    event_text: str


class WorkflowResponse(BaseModel):
    id: int
    user_id: UUID
    type: WorkflowType
    status: WorkflowStatus
    context: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class WorkflowStep(BaseModel):
    workflow_id: int
    step_order: int
    tool_called: str
    output: dict[str, Any]
    status: str
    executed_at: datetime