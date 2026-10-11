DISPLAY_LACTATION = {
    "giving_milk": "Giving Milk",
    "not_giving_milk": "Not Giving Milk"
}

DISPLAY_HEALTH = {
    "none": "No Issues"
}

DISPLAY_LOAN_PURPOSE = {
    "purchase_cattle": "Purchase Cattle"
}


def format_lactation(value):

    return DISPLAY_LACTATION.get(
        value,
        value
    )


def format_health(value):

    return DISPLAY_HEALTH.get(
        value,
        value
    )


def format_loan_purpose(value):

    return DISPLAY_LOAN_PURPOSE.get(
        value,
        value
    )