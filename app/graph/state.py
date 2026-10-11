from typing import TypedDict, List, Optional

class CattleRecord(TypedDict):
    animal_id: int

    breed: Optional[str]

    age: Optional[float]

    lactation_status: Optional[str]

    daily_milk_yield: Optional[float]

    health_issues: Optional[str]

    muzzle_image: Optional[str]

class CurrentSlot(TypedDict):
    type: str
    record_id: Optional[int]
    field: str

class SurabhiState(TypedDict):
    # Workflow
    current_stage: str
    current_slot: Optional[CurrentSlot]

    # Language
    language: Optional[str]

    # Identity
    name: Optional[str]
    mobile_number: Optional[str]
    village_district: Optional[str]
    identity_confirmed: bool

    # Cattle Data
    cattle_count: Optional[int]
    cattle: List[CattleRecord]
    cattle_confirmed: bool

    # Intent
    intent: Optional[str]
    intent_confirmed: bool

    # Loan Path
    other_income: Optional[str]
    existing_loans: Optional[str]

    loan_purpose: Optional[str]
    loan_amount: Optional[str]
    land_held: Optional[str]
    financial_confirmed: bool

    # Conversation
    latest_user_message: Optional[str]

    awaiting_correction_data: bool
    mobile_validation_failed: bool
    image_validation_failed: bool

    response: Optional[str]


