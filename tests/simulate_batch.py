
from copy import deepcopy

from app.main import state as initial_state, llm

from app.services.extractor import extract_updates
from app.services.state_manager import merge_state

from app.nodes.greeting import greeting_node
from app.nodes.identity import identity_node
from app.nodes.identity_confirmation import identity_confirmation_node
from app.nodes.cattle_data import cattle_data_node
from app.nodes.cattle_confirmation import cattle_confirmation_node
from app.nodes.intent_resolution import intent_resolution_node
from app.nodes.financial_data import financial_data_node
from app.nodes.financial_confirmation import financial_confirmation_node

from app.graph.stages import (
    GREETING,
    IDENTITY,
    IDENTITY_CONFIRMATION,
    CATTLE_DATA,
    CATTLE_CONFIRMATION,
    INTENT_RESOLUTION,
    FINANCIAL_DATA,
    FINANCIAL_CONFIRMATION,
    LOAN_HANDOFF,
    SCORE_HANDOFF,
)


# --------------------------------------------------
# TEST CONFIGURATION
# --------------------------------------------------

TEST_NAME = "Kannada Romanized Loan Application"

TEST_INPUTS = [
    "loan beku",
    "Ravi",
    "9876543210",
    "Mandya",
    "haudu",

    # Animal 1
    "rendu pasu",
    "HF breed",
    "4 years",
    "15 litre",
    "problem illa",
    "image uploaded",

    # Animal 2
    "Jersey",
    "2 years",
    "haalu kodalla",
    "problem illa",
    "image uploaded",

    "haudu",

    # Financial details
    "salary 30000",
    "tractor loan ide",
    "hasu purchase maadakke loan beku",
    "5 lakh",
    "3 acre",
    "haudu",
]

CONFIRMATION_STAGES = {
    IDENTITY_CONFIRMATION,
    CATTLE_CONFIRMATION,
    FINANCIAL_CONFIRMATION,
}

TERMINAL_STAGES = {
    LOAN_HANDOFF,
    SCORE_HANDOFF,
}


# --------------------------------------------------
# STAGE DISPATCH
# --------------------------------------------------

def execute_current_stage(state):
    stage = state["current_stage"]

    if stage == GREETING:
        return greeting_node(state)

    elif stage == IDENTITY:
        return identity_node(state)

    elif stage == IDENTITY_CONFIRMATION:
        return identity_confirmation_node(state, llm)

    elif stage == CATTLE_DATA:
        return cattle_data_node(state)

    elif stage == CATTLE_CONFIRMATION:
        return cattle_confirmation_node(state, llm)

    elif stage == INTENT_RESOLUTION:
        return intent_resolution_node(state)

    elif stage == FINANCIAL_DATA:
        return financial_data_node(state)

    elif stage == FINANCIAL_CONFIRMATION:
        return financial_confirmation_node(state, llm)

    elif stage in TERMINAL_STAGES:
        return state

    raise ValueError(f"Unknown stage: {stage!r}")


# --------------------------------------------------
# AUTOMATED TEST RUNNER
# --------------------------------------------------

def run_test():
    state = deepcopy(initial_state)
    input_index = 0
    turn = 0
    errors = []
    transcript = []

    print("\n" + "=" * 60)
    print(f"SURABHI AUTOMATED TEST: {TEST_NAME}")
    print("=" * 60)

    try:
        state = execute_current_stage(state)
    except Exception as exc:
        print(f"\nFAIL: Initial node failed: {exc}")
        return False

    while True:
        turn += 1

        stage = state.get("current_stage")
        response = state.get("response", "")

        print(f"\n{'-' * 60}")
        print(f"TURN {turn} | STAGE: {stage}")
        print(f"\nBOT: {response}")

        transcript.append({
            "turn": turn,
            "stage": stage,
            "bot": response,
        })

        if stage in TERMINAL_STAGES:
            print("\n" + "=" * 60)
            print("TEST FINISHED: WORKFLOW HANDOFF REACHED")
            print(f"Final stage: {stage}")
            print(f"Inputs consumed: {input_index}/{len(TEST_INPUTS)}")
            print("=" * 60)

            if input_index < len(TEST_INPUTS):
                print(
                    "WARNING: Some predefined inputs were unused. "
                    "Check whether the workflow skipped a stage."
                )

            return stage == LOAN_HANDOFF

        if input_index >= len(TEST_INPUTS):
            print("\nFAIL: Test inputs exhausted before handoff.")
            print(f"Stopped at stage: {stage}")
            return False

        user_message = TEST_INPUTS[input_index]
        input_index += 1

        print(f"\nTEST USER: {user_message}")

        state["latest_user_message"] = user_message

        try:
            # Handle data supplied after a rejected confirmation.
            if state.get("awaiting_correction_data"):
                updates = extract_updates(state, user_message, llm)

                if not isinstance(updates, dict):
                    raise TypeError(
                        "Extractor did not return a dictionary."
                    )

                real_updates = {
                    key: value
                    for key, value in updates.items()
                    if key != "language" and value is not None
                }

                if not real_updates:
                    if updates.get("language"):
                        state = merge_state(
                            state,
                            {"language": updates["language"]},
                        )

                    print(
                        "\nWARNING: No correction extracted. "
                        "The next predefined input will be used."
                    )
                    continue

                state = merge_state(state, updates)
                state["awaiting_correction_data"] = False

                # Re-run the confirmation node so the summary is rebuilt
                # using the application's own confirmation logic.
                state = execute_current_stage(state)
                continue

            # Confirmation nodes interpret yes/no responses themselves.
            if stage not in CONFIRMATION_STAGES:
                updates = extract_updates(state, user_message, llm)

                if not isinstance(updates, dict):
                    raise TypeError(
                        "Extractor did not return a dictionary."
                    )

                state = merge_state(state, updates)

            state = execute_current_stage(state)

        except Exception as exc:
            errors.append({
                "turn": turn,
                "stage": stage,
                "error": str(exc),
            })

            print("\nFAIL: Exception during test.")
            print(f"Stage: {stage}")
            print(f"Error: {type(exc).__name__}: {exc}")
            return False

    # Defensive fallback; normally the loop returns earlier.
    return False


if __name__ == "__main__":
    passed = run_test()

    print("\n" + "=" * 60)
    print("FINAL RESULT:", "PASS" if passed else "FAIL")
    print("=" * 60)
