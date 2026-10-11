LANGUAGES = {

    "english": {

        # Greeting

        "greeting_intro":
            "Hello! I am Surabhi.\n\n"
            "Would you like to check your cattle score or apply for a loan?",

        # Identity

        "ask_name":
            "What is your name?",

        "ask_mobile":
            "What is your mobile number?",

        "ask_village":
            "Which village or district are you from?",

        "identity_summary":
            "Name: {name}\n"
            "Mobile: {mobile}\n"
            "Village/District: {village}\n\n"
            "Is this correct?",

        "identity_unclear":
            "Sorry, did you confirm the information or would you like to change something?",

        "invalid_mobile":
            "Please enter a valid 10-digit mobile number.",

        # Cattle

        "cattle_intro":
            "Okay. Let me ask a few questions about your cattle.\n\n",

        "ask_cattle_count":
            "How many cattle do you have?",

        "ask_breed":
            "What is the breed of cattle {id}?",

        "ask_age":
            "What is the age of cattle {id}?",

        "ask_lactation":
            "Is cattle {id} currently giving milk?",

        "ask_milk_yield":
            "How many litres of milk does cattle {id} produce per day?",

        "ask_health":
            "Does cattle {id} have any health issues?",

        "ask_muzzle":
            "Please upload a muzzle image of cattle {id}.",

        "invalid_image":
            "Please upload a valid image.",

        "cattle_summary_prompt":
            "Is this correct?",

        "cattle_unclear":
            "Sorry, would you like to confirm or modify these cattle details?",

        "confirm_next_animal":
            "Are you describing the next animal?",

        # Intent

        "ask_intent":
            "Would you like cattle scoring only or are you applying for a loan?",

        "score_handoff":
            "Routing to Cattle Intelligence Agent.",

        # Financial

        "financial_intro":
            "Okay. Let me ask a few questions about your income and loans.\n\n",

        "ask_other_income":
            "Do you have any other source of income?",

        "ask_existing_loans":
            "Do you currently have any loans?",

        "ask_loan_purpose":
            "What is the purpose of this loan?",

        "ask_loan_amount":
            "How much loan amount do you need?",

        "ask_land":
            "How much land do you own?",

        "financial_summary_prompt":
            "Is this correct?",

        "financial_unclear":
            "Sorry, would you like to confirm or modify these financial details?",

        "loan_handoff":
            "Routing to Loan Processing Agent.",
        "provide_correction":
            "Please provide the correct information.",

        "no_cattle":
            "At least one cattle is required to continue."
    },

    "tamil_romanized": {

        "greeting_intro":
            "Vanakkam! Naan Surabhi.\n\n"
            "Neenga unga maadugaloda score paakanuma illa loan-ku apply panna virumbureengala?",

        "ask_name":
            "Unga peyar enna?",

        "ask_mobile":
            "Unga mobile number sollunga.",

        "ask_village":
            "Neenga entha ooru illa district?",

        "identity_summary":
            "Peyar: {name}\n"
            "Mobile: {mobile}\n"
            "Village/District: {village}\n\n"
            "Ithu sariyaa?",

        "identity_unclear":
            "Mannikkunga. Indha vivarangal sariyaa illa maatram venuma?",
        
        "invalid_mobile":
            "Dayavu seithu sariyana 10 digit mobile number sollunga.",

        "cattle_intro":
            "Seri. Ippo unga maadugal pathi sila kelvigal kekkaren.\n\n",

        "ask_cattle_count":
            "Ungakitta motham ethana pasu irukku?",

        "ask_breed":
            "Pasu {id} oda breed enna?",

        "ask_age":
            "Pasu {id} oda vayasu evlo?",

        "ask_lactation":
            "Pasu {id} ippoluthu paal kudukkudha?",

        "ask_milk_yield":
            "Pasu {id} oru naaluku evlo litre paal kudukkum?",

        "ask_health":
            "Pasu {id} ku yedhavathu health problem irukka?",
        
        "confirm_next_animal":
            "Neenga adutha pasu oda vivarangal sollreengala?",

        "ask_muzzle":
            "Pasu {id} oda muzzle photo upload pannunga.",

        "cattle_summary_prompt":
            "Ithu sariyaa?",

        "cattle_unclear":
            "Mannikkunga. Indha cattle vivarangal sariyaa illa maatram venuma?",

        "invalid_image":
            "Dayavu seithu sariyana photo upload pannunga.",

        "ask_intent":
            "Neenga score mattum paakanuma illa loan-ku apply panna virumbureengala?",

        "score_handoff":
            "Cattle Intelligence Agent-ku route pannaren.",

        "financial_intro":
            "Seri. Ippo unga varumanam matrum kadan vivarangal ketkaren.\n\n",

        "ask_other_income":
            "Ungalukku vera varumanam yedhavathu irukka?",

        "ask_existing_loans":
            "Ippo yedhavathu loan irukka?",

        "ask_loan_purpose":
            "Indha loan etharkaga venum?",

        "ask_loan_amount":
            "Evlo loan amount venum?",

        "ask_land":
            "Evlo nilam vechirukeenga?",

        "financial_summary_prompt":
            "Ithu sariyaa?",

        "financial_unclear":
            "Financial vivarangal sariyaa illa maatram venuma?",

        "loan_handoff":
            "Loan pipeline-ku route pannaren.",
        "provide_correction":
            "Sariyana vivarathai sollunga.",

        "no_cattle":
            "Thodaravatharku kurainthathu oru pasu irukkanum."
    },
    "kannada_romanized": {

        "greeting_intro":
            "Namaskara! Naanu Surabhi.\n\n"
            "Neevu nimma hasugala score nodbekaa athava loan-ge apply maadbekaa?",

        "ask_name":
            "Nimma hesaru enu?",

        "ask_mobile":
            "Nimma mobile number heli.",

        "ask_village":
            "Neevu yaava ooru athava district inda bandiddira?",

        "identity_summary":
            "Hesaru: {name}\n"
            "Mobile: {mobile}\n"
            "Village/District: {village}\n\n"
            "Idu sari ideya?",

        "identity_unclear":
            "Kshamisi. Ee mahiti sari ideya athava badalavane beka?",

        "invalid_mobile":
            "Dayavittu sariyada 10-ankiya mobile number heli.",

        "cattle_intro":
            "Sari. Iga nimma hasugala bagge kelavu prashnegalu keluttene.\n\n",

        "ask_cattle_count":
            "Nimma hatra ottu eshtu hasu ide?",

        "ask_breed":
            "Hasu {id} na breed enu?",

        "ask_age":
            "Hasu {id} ge eshtu varsha?",

        "ask_lactation":
            "Hasu {id} iga haalu koduttideya?",

        "ask_milk_yield":
            "Hasu {id} ondu dinakke eshtu litre haalu kodutte?",

        "ask_health":
            "Hasu {id} ge yavudadaru aarogya samasya ideya?",

        "confirm_next_animal":
            "Neevu mundina hasuvina vivaragalannu heluttiddira?",

        "ask_muzzle":
            "Hasu {id} na muzzle photo upload madi.",

        "cattle_summary_prompt":
            "Idu sari ideya?",

        "cattle_unclear":
            "Kshamisi. Ee hasuvina vivaragalalli badalavane beka?",

        "invalid_image":
            "Dayavittu sariyada photo upload madi.",

        "ask_intent":
            "Neevu score matra nodbekaa athava loan-ge apply maadbekaa?",

        "score_handoff":
            "Cattle Intelligence Agent-ge route maaduttiddene.",

        "financial_intro":
            "Sari. Iga nimma aadaaya mattu loan bagge kelavu prashnegalu keluttene.\n\n",

        "ask_other_income":
            "Nimage bere aadaaya moola ideya?",

        "ask_existing_loans":
            "Igaagale yava loan ideya?",

        "ask_loan_purpose":
            "Ee loan yaava uddeshakke beku?",

        "ask_loan_amount":
            "Eshtu loan amount beku?",

        "ask_land":
            "Nimma hatra eshtu bhoomi ide?",

        "financial_summary_prompt":
            "Idu sari ideya?",

        "financial_unclear":
            "Financial vivaragalalli badalavane beka?",

        "loan_handoff":
            "Loan processing pipeline-ge route maaduttiddene.",

        "provide_correction":
            "Dayavittu sariyada mahiti heli.",

        "no_cattle":
            "Munduvareyalu kanishta ondu hasu irabeku."
    }
}

def get_text(
    state,
    key
):

    language = (
        state.get("language")
        or "tamil_romanized"
    )

    if language not in LANGUAGES:
        language = "tamil_romanized"

    return LANGUAGES[language][key]

