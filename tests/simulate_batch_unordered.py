
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


# ============================================================
# TEST CONFIGURATION
# ============================================================

TEST_NAME = "Multilingual Unordered Extraction Test"

CONFIRMATION_STAGES = {
    IDENTITY_CONFIRMATION,
    CATTLE_CONFIRMATION,
    FINANCIAL_CONFIRMATION,
}

TERMINAL_STAGES = {
    LOAN_HANDOFF,
    SCORE_HANDOFF,
}

# Intentionally mix English, Tamil Romanized and Kannada Romanized.
# Messages contain multiple fields and some details arrive early.

TEST_INPUTS = [
    # Intent + identity + financial information before it is requested
    (
        "loan beku. Naan Ravi. My mobile number is 9876543210, "
        "Mandya district. Monthly salary 30000 irukku. "
        "Tractor loan ide. Hasu purchase maadakke 5 lakh beku. "
        "3 acre nilam vechirukken."
    ),

    # Identity confirmation
    "aama, correct",

    # Cattle count
    "Nimma kelvige answer: rendu pasu irukku",

    # Animal 1: Kannada + English + Tamil
    (
        "First hasu HF breed, 4 years old. "
        "Oru naaluku 15 litre paal kodukkum. "
        "Health problem illa. Muzzle photo upload panniten."
    ),

    # Animal 2: Tamil + Kannada + English
    (
        "Second pasu Jersey breed, vayasu 2 years. "
        "Idu haalu kodalla. Aarogya samasya illa. "
        "Muzzle photo uploaded."
    ),

    # Cattle confirmation in Kannada Romanized
    "haudu",

    # Financial confirmation in Tamil Romanized
    "aama, ellam sari",
]


# ============================================================
# STAGE DISPATCH
# ============================================================

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

    raise ValueError(f"Unknown workflow stage: {stage!r}")


# ============================================================
# STATE DISPLAY
# ============================================================

def print_state_snapshot(state):
    print("\n[STATE SNAPSHOT]")

    fields = [
        "current_stage",
        "language",
        "intent",
        "name",
        "mobile_number",
        "village_district",
        "cattle_count",
        "other_income",
        "existing_loans",
        "loan_purpose",
        "loan_amount",
        "land_held",
        "current_slot",
    ]

    for field in fields:
        print(f"  {field}: {state.get(field)!r}")

    print("  cattle:")

    for animal in state.get("cattle", []):
        print(f"    {animal}")


# ============================================================
# ASSERTIONS
# ============================================================

def normalize(value):
    if value is None:
        return ""

    return str(value).strip().lower()


def find_animal(state, breed):
    for animal in state.get("cattle", []):
        if normalize(animal.get("breed")) == normalize(breed):
            return animal

    return None


def check(label, condition, actual=None):
    print(f"[{'PASS' if condition else 'FAIL'}] {label}")

    if not condition and actual is not None:
        print(f"       Actual: {actual!r}")

    return condition


def run_assertions(state):
    print("\n" + "=" * 60)
    print("EXTRACTION AND SLOT-FILLING RESULTS")
    print("=" * 60)

    results = []

    results.append(check(
        "Name = Ravi",
        normalize(state.get("name")) == "ravi",
        state.get("name"),
    ))

    results.append(check(
        "Mobile number extracted correctly",
        normalize(state.get("mobile_number")) == "9876543210",
        state.get("mobile_number"),
    ))

    results.append(check(
        "Village/district = Mandya",
        normalize(state.get("village_district")) == "mandya",
        state.get("village_district"),
    ))

    results.append(check(
        "Loan intent identified",
        normalize(state.get("intent")) == "loan_application",
        state.get("intent"),
    ))

    results.append(check(
        "Other income populated",
        state.get("other_income") is not None,
        state.get("other_income"),
    ))

    results.append(check(
        "Existing loan information populated",
        state.get("existing_loans") is not None,
        state.get("existing_loans"),
    ))

    results.append(check(
        "Loan purpose populated",
        state.get("loan_purpose") is not None,
        state.get("loan_purpose"),
    ))

    amount = normalize(state.get("loan_amount")).replace(",", "")

    results.append(check(
        "Loan amount = 500000",
        amount in {"500000", "500000.0", "5 lakh", "5 lakhs"},
        state.get("loan_amount"),
    ))

    land = normalize(state.get("land_held"))

    results.append(check(
        "Landholding = 3 acres",
        land in {"3", "3.0", "3 acre", "3 acres"},
        state.get("land_held"),
    ))

    cattle = state.get("cattle", [])

    results.append(check(
        "Exactly two cattle records",
        len(cattle) == 2,
        cattle,
    ))

    hf = find_animal(state, "HF")
    jersey = find_animal(state, "Jersey")

    results.append(check(
        "HF record exists",
        hf is not None,
        hf,
    ))

    results.append(check(
        "Jersey record exists",
        jersey is not None,
        jersey,
    ))

    if hf:
        results.append(check(
            "HF age = 4",
            normalize(hf.get("age")) in {"4", "4.0"},
            hf.get("age"),
        ))

        results.append(check(
            "HF daily milk yield = 15",
            normalize(hf.get("daily_milk_yield")) in {"15", "15.0"},
            hf.get("daily_milk_yield"),
        ))

    if jersey:
        results.append(check(
            "Jersey age = 2",
            normalize(jersey.get("age")) in {"2", "2.0"},
            jersey.get("age"),
        ))

        results.append(check(
            "Jersey is not giving milk",
            normalize(jersey.get("lactation_status"))
            == "not_giving_milk",
            jersey.get("lactation_status"),
        ))

        results.append(check(
            "Jersey daily milk yield = 0",
            normalize(jersey.get("daily_milk_yield"))
            in {"0", "0.0"},
            jersey.get("daily_milk_yield"),
        ))

    passed = sum(results)
    total = len(results)

    print(f"\nRESULT: {passed}/{total} assertions passed.")

    return passed == total


# ============================================================
# TEST RUNNER
# ============================================================

def main():
    state = deepcopy(initial_state)
    input_index = 0
    turn = 0

    print("\n" + "=" * 60)
    print(TEST_NAME)
    print("=" * 60)

    try:
        state = execute_current_stage(state)
    except Exception as exc:
        print(f"Startup error: {type(exc).__name__}: {exc}")
        return

    while True:
        stage = state.get("current_stage")

        print("\n" + "-" * 60)
        print(f"TURN {turn + 1} | STAGE: {stage}")
        print("-" * 60)
        print("\nBOT:")
        print(state.get("response", ""))

        if stage in TERMINAL_STAGES:
            print(f"\nHANDOFF REACHED: {stage}")
            break

        if input_index >= len(TEST_INPUTS):
            print("\nTEST INPUTS EXHAUSTED BEFORE HANDOFF.")
            print_state_snapshot(state)
            run_assertions(state)
            return

        message = TEST_INPUTS[input_index]
        input_index += 1
        turn += 1

        print(f"\nTEST USER: {message}")
        state["latest_user_message"] = message

        try:
            # Confirmation responses go through the confirmation nodes.
            if stage in CONFIRMATION_STAGES:
                state = execute_current_stage(state)

            else:
                updates = extract_updates(state, message, llm)

                if not isinstance(updates, dict):
                    raise TypeError(
                        "extract_updates() must return a dictionary."
                    )

                print("\n[EXTRACTED UPDATES]")
                print(updates)

                state = merge_state(state, updates)

                print_state_snapshot(state)

                state = execute_current_stage(state)

        except Exception as exc:
            print(f"\nERROR at stage {stage}")
            print(f"{type(exc).__name__}: {exc}")
            print_state_snapshot(state)
            run_assertions(state)
            return

    print_state_snapshot(state)

    assertions_passed = run_assertions(state)

    overall_passed = (
        state.get("current_stage") == LOAN_HANDOFF
        and assertions_passed
    )

    print("\n" + "=" * 60)
    print("OVERALL RESULT:", "PASS" if overall_passed else "FAIL")
    print("=" * 60)


if __name__ == "__main__":
    main()
