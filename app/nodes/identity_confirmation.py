from app.graph.stages import (
    CATTLE_DATA,
)

from app.nodes.cattle_data import (
    cattle_data_node
)

from app.services.language import (
    get_text
)

from app.services.state_manager import (
    merge_state
)

from app.services.confirmation_service import (
    evaluate_confirmation
)


IDENTITY_FIELDS = {
    "name",
    "mobile_number",
    "village_district"
}


def build_identity_summary(state):

    return get_text(
        state,
        "identity_summary"
    ).format(
        name=state["name"],
        mobile=state["mobile_number"],
        village=state["village_district"]
    )


def identity_confirmation_node(
    state,
    llm
):

    result = evaluate_confirmation(
        summary=build_identity_summary(
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
            "identity_confirmed"
        ] = True

        state["awaiting_correction_data"] = False

        state["current_stage"] = (
            CATTLE_DATA
        )

        result = cattle_data_node(
            state
        )

        result["response"] = (
            get_text(
                state,
                "cattle_intro"
            )
            + result["response"]
        )

        return result

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

        filtered_updates = {
            key: value
            for key, value in updates.items()
            if key in IDENTITY_FIELDS
        }

        merge_state(
            state,
            filtered_updates
        )

        return {
            **state,
            "response":
            build_identity_summary(
                state
            )
        }

    return {
        **state,
        "response":
        get_text(
            state,
            "identity_unclear"
        )
    }