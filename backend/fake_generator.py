"""
fake_generator.py
-----------------
Generates realistic fake values for detected PII entities.
Guarantees consistent, deterministic replacement across the entire document
and repeated runs.
"""

from faker import Faker
import hashlib

# Cache for entity mappings during runtime
entity_map = {}


def _get_seeded_faker(original_text: str) -> Faker:
    """Creates a Faker instance seeded deterministically by the original text."""
    normalized = original_text.strip().lower()
    seed_int = int(hashlib.md5(normalized.encode('utf-8')).hexdigest(), 16) % (2**32)
    fake = Faker()
    Faker.seed(seed_int)
    return fake


def get_fake_value(entity_type: str, original: str) -> str:
    """
    Returns a realistic fake replacement for a detected PII entity.
    Consistent across identical entity occurrences.
    """
    key = original.strip()
    if not key:
        return original

    if key in entity_map:
        return entity_map[key]

    fake = _get_seeded_faker(key)

    if entity_type == "PERSON":
        value = fake.name()

    elif entity_type == "EMAIL_ADDRESS":
        # Extract username if available to match person fake if possible
        if "@" in key:
            local_part = key.split("@")[0]
            clean_name = local_part.replace(".", " ").replace("_", " ")
            person_fake = _get_seeded_faker(clean_name).name()
            username = person_fake.lower().replace(" ", ".")
            domain = fake.free_email_domain()
            value = f"{username}@{domain}"
        else:
            value = fake.email()

    elif entity_type == "PHONE_NUMBER":
        # Always generate a clean, uniform +91 phone number format
        digits = str(fake.random_number(digits=10, fix_len=True))
        value = f"+91 {digits[:5]} {digits[5:]}"

    elif entity_type in ("LOCATION", "ADDRESS"):
        raw_address = fake.address().replace("\n", ", ")
        value = f"{raw_address}"

    elif entity_type in ("COMPANY", "ORGANIZATION"):
        value = fake.company() + " Ltd"

    elif entity_type in ("SSN", "US_SSN"):
        value = fake.ssn()

    elif entity_type == "CREDIT_CARD":
        value = fake.credit_card_number(card_type=None)

    elif entity_type in ("DATE_OF_BIRTH", "DOB"):
        value = fake.date_of_birth().strftime("%d/%m/%Y")

    elif entity_type == "IP_ADDRESS":
        value = fake.ipv4()

    elif entity_type == "AADHAAR":
        digits = str(fake.random_number(digits=12, fix_len=True))
        value = f"{digits[:4]} {digits[4:8]} {digits[8:]}"

    else:
        # Generic fallback using Faker sentence/word if needed
        value = f"[REDACTED_{entity_type}]"

    entity_map[key] = value
    return value