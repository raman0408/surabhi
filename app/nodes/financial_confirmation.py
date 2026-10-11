from app.graph.stages import (
    LOAN_HANDOFF
)

from app.services.language import (
    get_text
)

from app.services.confirmation_service import (
    evaluate_confirmation
)
from app.services.display import (
    format_loan_purpose
)


FINANCIAL_FIELDS = {
    "other_income",
    "existing_loans",
    "loan_purpose",
    "loan_amount",
    "land_held"
}


def build_financial_summary(state):

    return (
        f"Other Income: {state['other_income']}\n"
        f"Existing Loans: {state['existing_loans']}\n"
        f"Loan Purpose: "
        f"{format_loan_purpose(state['loan_purpose'])}\n"
        f"Loan Amount: ₹{state['loan_amount']}\n"
        f"Land Held: {state['land_held']}"
    )


def financial_confirmation_node(
    state,
    llm
):

    result = evaluate_confirmation(
        summary=build_financial_summary(
            state
        ),
        user_message=state[
            "latest_user_message"
        ],
        llm=llm
    )

    status = result["status"]

    if status == "confirmed":

        state[
            "financial_confirmed"
        ] = True

        state[
            "awaiting_correction_data"
        ] = False

        state["current_stage"] = (
            LOAN_HANDOFF
        )

        return {
            **state,
            "response":
            get_text(
                state,
                "loan_handoff"
            )
        }

    if status == "rejected":

        updates = result.get(
            "updates",
            {}
        )

        if not updates:

            state[
                "awaiting_correction_data"
            ] = True

            return {
                **state,
                "response":
                get_text(
                    state,
                    "provide_correction"
                )
            }

        for key, value in updates.items():

            if key not in FINANCIAL_FIELDS:
                continue

            state[key] = value

        state[
            "awaiting_correction_data"
        ] = False

        return {
            **state,
            "response":
            (
                build_financial_summary(
                    state
                )
                + "\n\n"
                + get_text(
                    state,
                    "financial_summary_prompt"
                )
            )
        }

    return {
        **state,
        "response":
        get_text(
            state,
            "financial_unclear"
        )
    }