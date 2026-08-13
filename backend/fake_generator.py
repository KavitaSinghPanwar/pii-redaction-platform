from faker import Faker

fake = Faker()

entity_map = {}

def get_fake_value(entity_type, original):

    if original in entity_map:
        return entity_map[original]

    if entity_type == "PERSON":
        value = fake.name()

    elif entity_type == "EMAIL_ADDRESS":
        value = fake.email()

    elif entity_type == "PHONE_NUMBER":
        value = fake.phone_number()

    elif entity_type == "LOCATION":
        value = fake.address()

    else:
        value = f"<REDACTED_{entity_type}>"

    entity_map[original] = value
    return value