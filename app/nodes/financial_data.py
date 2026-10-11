# app/nodes/financial_data.py

from app.graph.stages import (
    FINANCIAL_CONFIRMATION
)
from app.nodes.financial_confirmation import (
    build_financial_summary
)
from app.services.slot_manager import (
    financial_complete,
    get_missing_financial_fields
)
from app.services.language import get_text


FIELD_KEYS = {
    "other_income": "ask_other_income",
    "existing_loans": "ask_existing_loans",
    "loan_purpose": "ask_loan_purpose",
    "loan_amount": "ask_loan_amount",
    "land_held": "ask_land"
}


def financial_data_node(state):

    if financial_complete(state):
        state["current_slot"] = None
        state["current_stage"] = FINANCIAL_CONFIRMATION

        summary = build_financial_summary(state)

        return {
            **state,
            "response":
            (
                summary 
                + "\n\n"
                + get_text(
                    state,
                    "financial_summary_prompt"
                )
            )
        }

    missing = get_missing_financial_fields(
        state
    )

    next_field = missing[0]

    question = get_text(
        state,
        FIELD_KEYS[next_field]
    )

    return {
        **state,
        "current_slot": {
            "type": "financial",
            "record_id": None,
            "field": next_field
        },
        "response": question
    }