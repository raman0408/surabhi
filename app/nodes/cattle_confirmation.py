from app.graph.stages import (
    INTENT_RESOLUTION
)

from app.services.display import (
    format_lactation,
    format_health
)

from app.nodes.intent_resolution import (
    intent_resolution_node
)

from app.services.language import (
    get_text
)

from app.services.confirmation_service import (
    evaluate_confirmation
)


def build_cattle_summary(state):

    lines = []

    for animal in state["cattle"]:

        lines.append(
            (
                f"Cattle {animal['animal_id']}\n"
                f"Breed: {animal['breed']}\n"
                f"Age: {animal['age']}\n"
                f"Lactation: "
                f"{format_lactation(animal['lactation_status'])}\n"
                f"Milk Yield: "
                f"{animal['daily_milk_yield']} litres\n"
                f"Health Issues: "
                f"{format_health(animal['health_issues'])}"
            )
        )

    return "\n\n".join(lines)

def cattle_confirmation_node(
    state,
    llm
):

    result = evaluate_confirmation(
        summary=build_cattle_summary(state),
        user_message=state["latest_user_message"],
        llm=llm
    )

    status = result["status"]

    if status == "confirmed":

        state["cattle_confirmed"] = True

        state["awaiting_correction_data"] = False

        state["current_stage"] = INTENT_RESOLUTION

        return intent_resolution_node(
            state
        )

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

        animal_id = updates.pop(
            "animal_id",
            None
        )

        if (
            animal_id is None
            and len(state["cattle"]) == 1
        ):
            animal_id = 1

        if animal_id:

            for animal in state["cattle"]:

                if (
                    animal["animal_id"]
                    == animal_id
                ):

                    animal.update(
                        updates
                    )

                    break

        state[
            "awaiting_correction_data"
        ] = False

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

    return {
        **state,
        "response":
        get_text(
            state,
            "cattle_unclear"
        )
    }