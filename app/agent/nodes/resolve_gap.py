nodes/gap_resolver.py
function	what it does	tech
resolve_gap(state)	LangGraph node. Takes first missing field, generates a friendly question, writes pending_question into state, sets status AWAITING_CONTEXT, calls interrupt(). Graph pauses here until answer_workflow() is called.
LangGraph
Python
build_question_for_field(field_name, workflow_type)	Pure function. Maps field name to India-contextual question. e.g. "pan_number" → "What's your PAN number?" / "current_city" → "Which city are you currently in?"
Python
inject_answer(state, field_name, answer)	Validates user's answer, writes it into state.life_state, removes field from missing_fields. Called when graph resumes from interrupt.