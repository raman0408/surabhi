from app.graph.workflow import build_graph

from app.services.extractor import extract_updates

from app.services.state_manager import merge_state

from app.llm.factory import get_llm

llm = get_llm()

graph = build_graph()

def create_initial_state():
    return {
        "current_stage": "greeting",
        "current_slot": None,

        "language": None,

        "intent": None,
        "intent_confirmed": False,

        "name": None,
        "mobile_number": None,
        "village_district": None,

        "identity_confirmed": False,

        "cattle_count": None,
        "cattle": [],

        "cattle_confirmed": False,

        "other_income": None,
        "existing_loans": None,

        "loan_purpose": None,
        "loan_amount": None,
        "land_held": None,

        "financial_confirmed": False,

        "latest_user_message": None,
        "awaiting_correction_data": False,
        "mobile_validation_failed": False,
        "image_validation_failed": False,

        "response": None
    }

state = create_initial_state()

