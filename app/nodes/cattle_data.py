from app.graph.stages import (
    CATTLE_CONFIRMATION
)

from app.nodes.cattle_confirmation import (
    build_cattle_summary
)

from app.services.language import (
    get_text
)

from app.services.slot_manager import (
    cattle_complete,
    get_next_incomplete_animal,
    get_missing_animal_fields
)


FIELD_KEYS = {
    "breed": "ask_breed",
    "age": "ask_age",
    "lactation_status": "ask_lactation",
    "daily_milk_yield": "ask_milk_yield",
    "health_issues": "ask_health",
    "muzzle_image": "ask_muzzle"
}


def cattle_data_node(state):

    if state.get("cattle_count") is None:

        return {
            **state,
            "response":
            get_text(
                state,
                "ask_cattle_count"
            )
        }

    # NEW: handle zero cattle
    if state["cattle_count"] == 0:

        return {
            **state,
            "response":
            get_text(
                state,
                "no_cattle"
            )
        }

    if len(state["cattle"]) == 0:

        state["cattle"] = [
            {
                "animal_id": i + 1,
                "breed": None,
                "age": None,
                "lactation_status": None,
                "daily_milk_yield": None,
                "health_issues": None,
                "muzzle_image": None
            }
            for i in range(
                state["cattle_count"]
            )
        ]
    if state.get(
        "image_validation_failed"
    ):

        return {
            **state,
            "response": get_text(
                state,
                "invalid_image"
            )
        }

    if cattle_complete(state):

        state["current_slot"] = None
        state["current_stage"] = (
            CATTLE_CONFIRMATION
        )

        summary = build_cattle_summary(
            state
        )

        return {
            **state,
            "response":
            (
                summary
                + "\n\n"
                + get_text(
                    state,
                    "cattle_summary_prompt"
                )
            )
        }

    animal = get_next_incomplete_animal(
        state
    )

    # Defensive guard
    if animal is None:

        raise Exception(
            (
                "cattle_count > 0 "
                "but no incomplete animal found."
            )
        )

    missing = get_missing_animal_fields(
        animal
    )

    next_field = missing[0]

    question = get_text(
        state,
        FIELD_KEYS[next_field]
    ).format(
        id=animal["animal_id"]
    )

    return {
        **state,
        "current_slot": {
            "type": "cattle",
            "record_id":
                animal["animal_id"],
            "field":
                next_field
        },
        "response": question
    }