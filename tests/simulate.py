from app.main import state, llm

from app.services.extractor import extract_updates
from app.services.state_manager import merge_state
from app.nodes.financial_data import (
    financial_data_node
)

from app.nodes.financial_confirmation import (
    financial_confirmation_node
)
from app.nodes.greeting import greeting_node
from app.nodes.identity import identity_node
from app.nodes.identity_confirmation import (
    identity_confirmation_node
)

from app.nodes.cattle_data import (
    cattle_data_node
)
from app.nodes.intent_resolution import (
    intent_resolution_node
)
from app.nodes.cattle_confirmation import (
    cattle_confirmation_node
)

from app.graph.stages import (
    GREETING,
    IDENTITY,
    IDENTITY_CONFIRMATION,
    CATTLE_DATA,
    CATTLE_CONFIRMATION,
    INTENT_RESOLUTION,
    FINANCIAL_CONFIRMATION,
    FINANCIAL_DATA,
    LOAN_HANDOFF,
    SCORE_HANDOFF
)


def execute_current_stage(state):

    stage = state["current_stage"]

    if stage == GREETING:
        return greeting_node(state)

    if stage == IDENTITY:
        return identity_node(state)

    if stage == IDENTITY_CONFIRMATION:
        return identity_confirmation_node(
            state,
            llm
        )

    if stage == CATTLE_DATA:
        return cattle_data_node(state)

    if stage == CATTLE_CONFIRMATION:
        return cattle_confirmation_node(
            state,
            llm
        )
    if stage == INTENT_RESOLUTION:
        return intent_resolution_node(state)
    
    if stage == FINANCIAL_DATA:
        return financial_data_node(state)

    if stage == FINANCIAL_CONFIRMATION:
        return financial_confirmation_node(
            state,
            llm
        )


    return state




print("\n===== SURABHI TEST =====\n")

state = execute_current_stage(state)

while True:

    print("\nBOT:")
    print(state["response"])

    if state["current_stage"] in {
        LOAN_HANDOFF,
        SCORE_HANDOFF
    }:
        break

    user_message = input("\nYOU: ")
    if user_message.lower() == "exit":
        break
    state["latest_user_message"] = user_message

    CONFIRMATION_STAGES = {
        IDENTITY_CONFIRMATION,
        CATTLE_CONFIRMATION,
        FINANCIAL_CONFIRMATION
    }

    if state.get(
        "awaiting_correction_data"
    ):

        updates = extract_updates(
            state,
            user_message,
            llm
        )

        real_updates = {
            k: v
            for k, v in updates.items()
            if k != "language"
        }


        if real_updates:

            merge_state(
                state,
                real_updates
            )

            state[
                "awaiting_correction_data"
            ] = False

            if (
                state["current_stage"]
                == IDENTITY_CONFIRMATION
            ):

                from app.nodes.identity_confirmation import (
                    build_identity_summary
                )

                state["response"] = (
                    build_identity_summary(
                        state
                    )
                )

            elif (
                state["current_stage"]
                == CATTLE_CONFIRMATION
            ):

                from app.nodes.cattle_confirmation import (
                    build_cattle_summary
                )

                state["response"] = (
                    build_cattle_summary(
                        state
                    )
                    + "\n\n"
                    + state["response"]
                )

            elif (
                state["current_stage"]
                == FINANCIAL_CONFIRMATION
            ):

                from app.nodes.financial_confirmation import (
                    build_financial_summary
                )

                state["response"] = (
                    build_financial_summary(
                        state
                    )
                )

            print("\nUPDATED SUMMARY:")
            print(state["response"])

            continue

    if state["current_stage"] not in CONFIRMATION_STAGES:
        try:

            updates = extract_updates(
                state,
                user_message,
                llm
            )

            state = merge_state(
                state,
                updates
            )

        except Exception as e:

            print("\nEXTRACTION ERROR:")
            print(e)

            break    

    state = execute_current_stage(
        state
    )

    print("\nCURRENT STAGE:")
    print(state["current_stage"])

    print("\nSTATE SNAPSHOT:")
    print({
        "name": state["name"],
        "mobile": state["mobile_number"],
        "village": state["village_district"],
        "intent": state["intent"],
        "cattle_count": state["cattle_count"]
    })
    print("\nFULL CATTLE STATE:")
    print(state["cattle"])

    print("\nFULL FINANCIAL STATE")
    print({
        "other_income": state["other_income"],
        "existing_loans": state["existing_loans"],

        "loan_purpose": state["loan_purpose"],
        "loan_amount": state["loan_amount"],
        "land_held": state["land_held"],
        "financial_confirmed": state["financial_confirmed"]
    })