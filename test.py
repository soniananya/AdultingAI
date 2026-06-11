"""from app.agent.graph import build_main_graph
from app.agent.state import (
    LifeStateSnapshot
)
from app.models.workflow import (
    WorkflowType
)

graph = build_main_graph()

state = {

    "user_id": "123",

    "workflow_id": 1,

    "workflow_type":
        WorkflowType.JD_ANALYSIS,

    "life_state":
        LifeStateSnapshot(
            current_salary=None,
            employer=None,
            monthly_rent=None,
            current_city=None,
            housing_type=None,
            employment_type=None,
            joining_date=None,
            recurring_bills=[],
            resume_url=None,
            skills=[]
        ),

    "messages": [],

    "pending_life_state_updates": {},

    "pending_reminders": [],

    "pending_artifacts": [],

    "errors": [],

    "hitl_approved": None,

    "pending_action": None,
}

result = graph.invoke(state)

print(result)"""
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("SUPABASE_URL"))
print(os.getenv("SUPABASE_KEY"))