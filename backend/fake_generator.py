from faker import Faker
import random

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
        value = (
            "+91 "
            + str(random.randint(
                6000000000,
                9999999999
            ))
        )

    elif entity_type == "LOCATION":
        value = fake.address().replace(
            "\n",
            ", "
        )

    elif entity_type == "CREDIT_CARD":
        value = fake.credit_card_number()

    elif entity_type == "IP_ADDRESS":
        value = fake.ipv4()
    elif entity_type == "AADHAAR":
        value = "XXXX XXXX XXXX"

    else:
        value = original

    entity_map[original] = value

    return value