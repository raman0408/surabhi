from app.services.slot_manager import (
    identity_complete,
    get_missing_identity_fields,
)

from app.services.language import (
    get_text
)

from app.graph.stages import (
    IDENTITY_CONFIRMATION
)


FIELD_KEYS = {
    "name": "ask_name",
    "mobile_number": "ask_mobile",
    "village_district": "ask_village"
}


def identity_node(state):
    """
    Identity Collection Node

    Assumptions:
    - latest_user_message has already been processed by extractor.py
    - state already contains any newly extracted values

    Responsibilities:
    - Determine missing identity fields
    - Ask next question
    - Route to confirmation when complete
    """
    if state.get(
        "mobile_validation_failed"
    ):

        return {
            **state,
            "response": get_text(
                state,
                "invalid_mobile"
            )
        }
    
    if identity_complete(state):

        state["current_slot"] = None
        state["current_stage"] = IDENTITY_CONFIRMATION

        return {
            **state,
            "response": get_text(
                state,
                "identity_summary"
            ).format(
                name=state["name"],
                mobile=state["mobile_number"],
                village=state["village_district"]
            )
        }

    missing_fields = get_missing_identity_fields(
        state
    )

    next_field = missing_fields[0]

    return {
        **state,
        "current_slot": {
            "type": "identity",
            "record_id": None,
            "field": next_field
        },
        "response": get_text(
            state,
            FIELD_KEYS[next_field]
        )
    }