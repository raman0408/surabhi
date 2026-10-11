def identity_complete(state):
    return all([
        state.get("name"),
        state.get("mobile_number"),
        state.get("village_district")
    ])

def cattle_complete(state):
    cattle_count = state.get("cattle_count")

    if not cattle_count:
        return False
    
    cattle = state.get("cattle", [])

    if len(cattle) != cattle_count:
        return False
    
    for animal in cattle:
        required_fields = [
            "breed",
            "age",
            "lactation_status",
            "daily_milk_yield",
            "health_issues",
            "muzzle_image"
        ]
        for field in required_fields:

            if animal.get(field) is None:
                return False
    return True

def financial_complete(state):
    required = [
        "other_income",
        "existing_loans",
        "loan_purpose",
        "loan_amount",
        "land_held"
    ]

    for field in required:
        if state.get(field) is None:
            return False

    return True

def intent_known(state):
    return state.get("intent") is not None

def get_missing_identity_fields(state):
    missing = []

    if state.get("name") is None:
        missing.append("name")
    
    if state.get("mobile_number") is None:
        missing.append("mobile_number")

    if state.get("village_district") is None:
        missing.append("village_district")
    
    return missing

def get_missing_animal_fields(animal):

    missing = []

    if animal.get("breed") is None:
        missing.append("breed")

    if animal.get("age") is None:
        missing.append("age")

    if animal.get("lactation_status") is None:
        missing.append("lactation_status")

    if animal.get("daily_milk_yield") is None:
        missing.append("daily_milk_yield")

    if animal.get("health_issues") is None:
        missing.append("health_issues")

    if animal.get("muzzle_image") is None:
        missing.append("muzzle_image")

    return missing

def get_next_incomplete_animal(state):

    cattle = state.get("cattle", [])

    for animal in cattle:

        if get_missing_animal_fields(animal):
            return animal

    return None


def get_missing_financial_fields(state):

    missing = []

    if state.get("other_income") is None:
        missing.append("other_income")

    if state.get("existing_loans") is None:
        missing.append("existing_loans")

    if state.get("loan_purpose") is None:
        missing.append("loan_purpose")

    if state.get("loan_amount") is None:
        missing.append("loan_amount")

    if state.get("land_held") is None:
        missing.append("land_held")

    return missing
