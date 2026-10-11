ANIMAL_FIELDS = {
    "breed",
    "age",
    "lactation_status",
    "daily_milk_yield",
    "health_issues",
    "muzzle_image"
}
def is_valid_mobile(number):

    if not number:
        return False

    digits = "".join(
        c for c in str(number)
        if c.isdigit()
    )

    return (
        len(digits) == 10
        and digits[0] in "6789"
    )


def is_valid_image(value):

    return value == "uploaded"

def get_animal_by_id(
    state,
    animal_id
):

    for animal in state.get("cattle", []):

        if animal["animal_id"] == animal_id:
            return animal

    return None





def merge_state(
    state,
    updates
):

    slot = state.get("current_slot")

    language = updates.pop(
        "language",
        None
    )

    if language:

        if language == "english":

            current_language = state.get("language")

            if current_language in {
                "tamil_romanized",
                "kannada_romanized"
            }:
                pass

            else:
                state["language"] = language

        else:
            state["language"] = language


    for key, value in updates.items():

        if value is None:
            continue

        if (
            slot
            and slot["type"] == "cattle"
            and key in ANIMAL_FIELDS
        ):

            animal = get_animal_by_id(
                state,
                slot["record_id"]
            )

            if animal:

                #
                # image validation
                #

                if key == "muzzle_image":

                    if is_valid_image(value):

                        animal["muzzle_image"] = value
                        state["image_validation_failed"] = False

                    else:

                        state["image_validation_failed"] = True

                else:

                    animal[key] = value

                #
                # business rule
                #
                if (
                    updates.get("lactation_status")
                    == "not_giving_milk"
                ):

                    animal["daily_milk_yield"] = 0
                if (
                    updates.get("daily_milk_yield") is not None
                    and updates["daily_milk_yield"] > 0
                ):
                    animal["lactation_status"] = "giving_milk"

        else:

            if key == "mobile_number":

                if is_valid_mobile(value):

                    state["mobile_number"] = value
                    state["mobile_validation_failed"] = False

                else:

                    state["mobile_validation_failed"] = True

            else:

                state[key] = value

    return state