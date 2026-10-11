from app.graph.stages import (
    FINANCIAL_DATA,
    SCORE_HANDOFF
)

from app.services.language import (
    get_text
)

from app.nodes.financial_data import (
    financial_data_node
)


def intent_resolution_node(state):

    intent = state.get("intent")

    if intent == "loan_application":

        state["current_stage"] = FINANCIAL_DATA

        result = financial_data_node(
            state
        )

        result["response"] = (
            get_text(
                state,
                "financial_intro"
            )
            + result["response"]
        )

        return result

    if intent == "score_only":

        state["current_stage"] = (
            SCORE_HANDOFF
        )

        return {
            **state,
            "response":
            get_text(
                state,
                "score_handoff"
            )
        }

    return {
        **state,
        "current_slot": {
            "type": "intent",
            "record_id": None,
            "field": "intent"
        },
        "response":
        get_text(
            state,
            "ask_intent"
        )
    }