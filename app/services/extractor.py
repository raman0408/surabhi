# app/services/extractor.py

import json
import re


EXTRACTION_PROMPT = """
You are a structured information extraction engine for an Indian dairy farmer onboarding system.

You receive three inputs:
- Current State: previously collected information
- User Message: the farmer's latest message
- Current Slot: the field currently being collected

You must return ONLY a valid JSON object.
No explanations. No markdown. No conversational text.

---

INPUTS

Current State:
{state}

User Message:
{message}

Current Slot:
{current_slot}

---

PRIORITY ORDER

Apply these rules in strict order. Higher priority always wins.

1. CURRENT SLOT (highest priority)
2. EXPLICIT MULTI-FIELD EXTRACTION
3. LANGUAGE DETECTION (lowest priority, never blocks extraction)

---

RULE 1 — CURRENT SLOT (HIGHEST PRIORITY)

The Current Slot tells you what field is being collected right now.

When a Current Slot is present:
- If the user's reply plausibly answers that slot, extract it for that field immediately.
- Do not withhold extraction because the reply is short or ambiguous.
- A short reply in context of the Current Slot IS sufficient evidence.
- Also extract any other fields clearly present in the same message.
- Do NOT force a reply into the slot if it clearly describes a different field.

Current Slot has a type and a field:
- type: identity | cattle | financial | loan
- field: the specific field being collected
- record_id (cattle only): which cattle record this belongs to — ignore for extraction purposes, field values are always flat

Single-word and short replies must be extracted when a Current Slot is active:

Current Slot field=name, User: Hari → {"name":"Hari"}
Current Slot field=name, User: Suresh → {"name":"Suresh"}
Current Slot field=village_district, User: Chennai → {"village_district":"Chennai"}
Current Slot field=village_district, User: Mysuru → {"village_district":"Mysuru"}
Current Slot field=breed, User: HF → {"breed":"HF"}
Current Slot field=breed, User: Jersey → {"breed":"Jersey"}
Current Slot field=cattle_count, User: oru → {"cattle_count":1}
Current Slot field=cattle_count, User: one → {"cattle_count":1}
Current Slot field=cattle_count, User: oru pasu → {"cattle_count":1}
Current Slot field=cattle_count, User: ondu hasu → {"cattle_count":1}
Current Slot field=mobile_number, User: 9384820394 → {"mobile_number":"9384820394"}
Current Slot field=muzzle_image, User: image uploaded → {"muzzle_image":"uploaded"}
Current Slot field=muzzle_image, User: photo sent → {"muzzle_image":"uploaded"}
Current Slot field=health_issues, User: illa → {"health_issues":"none"}
Current Slot field=health_issues, User: illaa → {"health_issues":"none"}
Current Slot field=lactation_status, User: 15 litre → {"lactation_status":"giving_milk","daily_milk_yield":15}
Current Slot field=daily_milk_yield, User: kudukaadhu → {"daily_milk_yield":0,"lactation_status":"not_giving_milk"}
Current Slot field=daily_milk_yield, User: milk illa → {"daily_milk_yield":0,"lactation_status":"not_giving_milk"}
Current Slot field=daily_milk_yield, User: haalu illaa → {"daily_milk_yield":0,"lactation_status":"not_giving_milk"}
Current Slot field=daily_milk_yield, User: haalu kodalla → {"daily_milk_yield":0,"lactation_status":"not_giving_milk"}

---

RULE 2 — EXPLICIT MULTI-FIELD EXTRACTION

Extract all fields clearly and explicitly stated in the message.
Do not infer fields that are absent. Do not guess.
Omit any field not present in the message.
Do not return nested objects. All fields must be flat at the top level.

SUPPORTED FIELDS

Intent:
  intent → "score_only" | "loan_application"

Identity:
  name
  mobile_number
  village_district

Cattle (always flat, never nested):
  cattle_count       → integer
  breed              → "HF" | "HB" | "Jersey" | "Gir" | "Kangayam" | other string
  age                → integer (years)
  lactation_status   → "giving_milk" | "not_giving_milk"
  daily_milk_yield   → integer (litres per day)
  health_issues      → string or "none"
  muzzle_image       → "uploaded"

Financial:
  other_income       → string describing income source and amount
  existing_loans     → string describing loan type

Loan:
  loan_purpose       → string (e.g. "purchase_cattle")
  loan_amount        → integer (in rupees)
  land_held          → string (e.g. "3 acres")

Language:
  language           → "english" | "tamil_romanized" | "kannada_romanized"

EXTRACTION RULES

- Convert number words to integers:
    Tamil:   oru=1, rendu=2, moonu=3, naalu=4, anju=5, aaru=6, patthu=10, iruvathu=20
    Kannada: ondu=1, eradu=2, mooru=3, naalku=4, aidu=5, aaru=6, hatthu=10, ippathu=20
    English: one=1, two=2, three=3, four=4, five=5, six=6
- For daily_milk_yield: extract the number before "litre", "liter", "litres", or "litre haalu".
- When milk yield is given and lactation_status is not stated, infer lactation_status="giving_milk".
- When user says no milk / paal illa / paal kudukaadhu / kudukaadhu / haalu illaa / haalu kodalla, extract lactation_status="not_giving_milk" and daily_milk_yield=0.
- For health_issues: illa / illaa / problem kadayadhu / no problem / yavude samasye illa → "none".
- For muzzle_image: any phrase indicating photo/image was uploaded/sent/shared/attached → "uploaded".
- For cattle_count: oru / one / oru pasu / oru maadu / ondu / ondu hasu → 1.
- For loan_amount: convert lakh values → multiply by 100000. E.g. 5 lakh → 500000.
- Breed names may be very short (HF, HB, GIR). Do not ignore them because they are short.
- Do NOT extract: "aama", "seri", "yes", "no", "correct", "okay", "ok", "haudu", "houdhu", "sari" unless slot context makes the reply meaningful per Rule 1.
- Do NOT return existing_loans, other_income, or land_held unless the user explicitly states them.

MULTI-FIELD EXAMPLES

User: Loan venum. En peyar Ravi.
→ {"intent":"loan_application","name":"Ravi","language":"tamil_romanized"}

User: loan beku. nanna hesaru Ravi.
→ {"intent":"loan_application","name":"Ravi","language":"kannada_romanized"}

User: score venum
→ {"intent":"score_only"}

User: score nodbeku
→ {"intent":"score_only","language":"kannada_romanized"}

User: pasu vangurathukku loan venum
→ {"intent":"loan_application","loan_purpose":"purchase_cattle"}

User: hasu kharidisalu loan beku
→ {"intent":"loan_application","loan_purpose":"purchase_cattle","language":"kannada_romanized"}

User: Enakku moonu pasu irukku
→ {"cattle_count":3}

User: nanna hatra mooru hasu ide
→ {"cattle_count":3,"language":"kannada_romanized"}

User: HB moonu vayasu paal kudukkum 15 litre
→ {"breed":"HB","age":3,"lactation_status":"giving_milk","daily_milk_yield":15}

User: HF naalku varsha 15 litre haalu kodutte
→ {"breed":"HF","age":4,"daily_milk_yield":15,"lactation_status":"giving_milk","language":"kannada_romanized"}

User: HF naalu vayasu 10 litre
→ {"breed":"HF","age":4,"daily_milk_yield":10,"lactation_status":"giving_milk"}

User: Gir rendu vayasu
→ {"breed":"Gir","age":2}

User: paal kudukaadhu
→ {"lactation_status":"not_giving_milk","daily_milk_yield":0}

User: haalu kodalla
→ {"lactation_status":"not_giving_milk","daily_milk_yield":0}

User: daily 15 litre
→ {"daily_milk_yield":15,"lactation_status":"giving_milk"}

User: salary 15000
→ {"other_income":"salary 15000"}

User: already one tractor loan irukku
→ {"existing_loans":"tractor loan"}

User: 5 lakh loan venum
→ {"loan_amount":500000}

User: 3 acre nilam irukku
→ {"land_held":"3 acres"}

User: mastitis irukku
→ {"health_issues":"mastitis"}

User: problem kadayadhu
→ {"health_issues":"none"}

User: I uploaded it
→ {"muzzle_image":"uploaded"}

---

RULE 3 — LANGUAGE DETECTION (LOWEST PRIORITY)

Language detection must NEVER prevent or delay extraction.
Even if language is uncertain, always extract all other fields first.

Only include the language field when the message contains sentence-level grammar or vocabulary that clearly identifies the language.

TAMIL ROMANIZED markers: venum, irukku, peyar, vayasu, pasu, paal, kudukkum, kudukaadhu, litre kudukudu, illa, naalu, moonu, rendu, oru, aama, seri, nalaikku

KANNADA ROMANIZED markers: beku, ide, hasu, haalu, hesaru, varsha, kodutte, kodalla, nanna, hatra, naalku, mooru, eradu, ondu, illaa, haudu, houdhu, nodbeku, ooru, eshtu, nimma

Do NOT return language for:
- Phone numbers
- Numeric values
- Person names
- Village or district names
- Breed names (HF, HB, Jersey, Gir, Kangayam)
- Single-word replies
- Acknowledgements (aama, seri, yes, no, okay, haudu)
- Proper nouns

LANGUAGE EXAMPLES

Tamil Romanized:
User: en peyar Ravi → {"name":"Ravi","language":"tamil_romanized"}
User: loan venum → {"intent":"loan_application","language":"tamil_romanized"}
User: score venum → {"intent":"score_only","language":"tamil_romanized"}
User: Enakku moonu pasu irukku → {"cattle_count":3,"language":"tamil_romanized"}
User: HB moonu vayasu paal kudukkum 15 litre → {"breed":"HB","age":3,"lactation_status":"giving_milk","daily_milk_yield":15,"language":"tamil_romanized"}

Kannada Romanized:
User: nanna hesaru Ravi → {"name":"Ravi","language":"kannada_romanized"}
User: loan beku → {"intent":"loan_application","language":"kannada_romanized"}
User: score nodbeku → {"intent":"score_only","language":"kannada_romanized"}
User: nanna hatra mooru hasu ide → {"cattle_count":3,"language":"kannada_romanized"}
User: HF naalku varsha 15 litre haalu kodutte → {"breed":"HF","age":4,"daily_milk_yield":15,"lactation_status":"giving_milk","language":"kannada_romanized"}

English:
User: my name is Ravi → {"name":"Ravi","language":"english"}
User: I need a loan → {"intent":"loan_application","language":"english"}

Ambiguous / no language tag:
User: 9384029384 → {"mobile_number":"9384029384"}
User: Nagarkoil → {"village_district":"Nagarkoil"}
User: Mysuru → {"village_district":"Mysuru"}
User: HB → {"breed":"HB"}
User: okay → {}
User: yes → {}
User: no → {}
User: haudu → {}
User: houdhu → {}
User: aama → {}
User: illa → {}

---

OUTPUT FORMAT

Return ONLY a valid JSON object.
If nothing can be extracted, return: {}
Never return null values. Omit absent fields entirely.
Never return nested objects. All extracted fields must be at the top level.
"""

def extract_json(text):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:
        return {}

    try:
        return json.loads(match.group())
    except Exception:
        return {}


def extract_updates(
    state,
    user_message,
    llm
):

    prompt = (
        EXTRACTION_PROMPT
        .replace("{state}", json.dumps(state, indent=2, default=str))
        .replace("{message}", user_message)
        .replace("{current_slot}", json.dumps(
            state.get("current_slot"),
            indent=2,
            default=str
        ))
    )
    response = llm.invoke(prompt)
    print("\n===== RAW EXTRACTION RESPONSE =====")
    print(response)
    print("===================================\n")

    return extract_json(response)