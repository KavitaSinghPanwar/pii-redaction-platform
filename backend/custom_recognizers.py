"""
custom_recognizers.py
---------------------
Defines custom Presidio recognizers for PII detection.
Covers 9 PII categories:
1. Full Names (PERSON)
2. Email Addresses (EMAIL_ADDRESS)
3. Phone Numbers (PHONE_NUMBER)
4. Company Names (COMPANY)
5. Physical/Mailing Addresses (ADDRESS)
6. Social Security Numbers (SSN)
7. Credit Card Numbers (CREDIT_CARD)
8. Dates of Birth (DATE_OF_BIRTH)
9. IP Addresses (IP_ADDRESS)

To add a new PII type, define a PatternRecognizer with supported_entity set to the new entity name
and add it to get_custom_recognizers().
"""

from presidio_analyzer import PatternRecognizer, Pattern

# List of known prospectus companies for precision recognizer
PROSPECTUS_COMPANIES = [
    "KSH INTERNATIONAL LIMITED",
    "KSH International Limited",
    "Nuvama Wealth Management Limited",
    "ICICI Securities Limited",
    "MUFG Intime India Private Limited",
    "Link Intime India Private Limited",
    "Kirtane & Pandit LLP",
    "Kirtane & Pandit, LLP",
    "CARE Analytics and Advisory Private Limited",
    "CareEdge Research",
    "Waterloo Motors Private Limited",
    "KSH Project Management Services Private Limited",
    "KSH Infra Park 5 Private Limited",
    "KSH Infra Park VI Private Limited",
    "KSH Distriparks Private Limited",
    "KSH Integrated Logistics Private Limited",
    "Kushal Motors and Electricals Private Limited",
    "Waterloo Industrial Park VI Private Limited",
    "HDFC Bank Limited",
    "ICICI Bank Limited",
    "Citibank N.A.",
    "Export-Import Bank of India",
    "State Bank of India",
    "Federal Bank Limited",
    "The Federal Bank Limited",
    "Bajaj Finance Limited",
    "Trilegal",
    "Dhaulagiri Family Trust",
    "Everest Family Trust",
    "Makalu Family Trust",
    "Broad Family Trust",
    "Annapurna Family Trust",
    "Kanchenjunga Family Trust",
    "Malabar India Fund Limited",
    "Hingne Tare & Associates"
]

# List of known prospectus names for precision recognizer
PROSPECTUS_NAMES = [
    "Kushal Subbayya Hegde",
    "KUSHAL SUBBAYYA HEGDE",
    "Pushpa Kushal Hegde",
    "PUSHPA KUSHAL HEGDE",
    "Rajesh Kushal Hegde",
    "RAJESH KUSHAL HEGDE",
    "Rohit Kushal Hegde",
    "ROHIT KUSHAL HEGDE",
    "Rakhi Girija Shetty",
    "RAKHI GIRIJA SHETTY",
    "Sarthak Malvadkar",
    "Sandesh Bhagwat",
    "Amod Joshi",
    "Dinesh Hirachand Munot",
    "Ajay Shriram Patil",
    "Ram Kumar Tiwari",
    "Indu Jacob",
    "Lokesh Shah",
    "Soumavo Sarkar",
    "Kishan Rastogi",
    "Abhijit Diwan",
    "Shanti Gopalkrishnan",
    "Lalit Muljibhai Sarvaiya",
    "Sugriv Singh",
    "Vishal Singh",
    "Parag Pansare",
    "Eric Bacha",
    "Sachin Gawade",
    "Pravin Teli",
    "Siddharth Jadhav",
    "Tushar Gavankar",
    "Hitesh Ramani",
    "Chitra Raste",
    "Sharmila Joshi",
    "Tushar Wakhele",
    "Ashish Mathew Pulloor",
    "Anand Soni",
    "Rupal K. Sancheti",
    "Salil Ajay Bhargava",
    "Jabeen Ajay Menon",
    "Ajay Menon",
    "Sunil Nagayya Shetty",
    "Maithili Rajesh Hegde",
    "Katyayani Balasubramanian",
    "Sangeeta Ramprasad Rai"
]


def get_custom_recognizers():
    """Returns a list of custom Presidio PatternRecognizers for all PII types."""
    import re
    recognizers = []

    # 1. Social Security Number (SSN)
    ssn_pattern = Pattern(
        name="ssn_regex",
        regex=r"\b\d{3}-\d{2}-\d{4}\b",
        score=0.95
    )
    recognizers.append(
        PatternRecognizer(
            supported_entity="SSN",
            patterns=[ssn_pattern]
        )
    )

    # 2. Credit Card Number
    credit_card_pattern = Pattern(
        name="credit_card_regex",
        regex=r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        score=0.95
    )
    recognizers.append(
        PatternRecognizer(
            supported_entity="CREDIT_CARD",
            patterns=[credit_card_pattern]
        )
    )

    # 3. IP Address
    ip_pattern = Pattern(
        name="ip_address_regex",
        regex=r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
        score=0.95
    )
    recognizers.append(
        PatternRecognizer(
            supported_entity="IP_ADDRESS",
            patterns=[ip_pattern]
        )
    )

    # 4. Date of Birth (DOB)
    dob_patterns = [
        Pattern(
            name="dob_slash_dash",
            regex=r"\b(?:0[1-9]|[12][0-9]|3[01])[/.-](?:0[1-9]|1[012])[/.-](?:19|20)\d{2}\b",
            score=0.90
        ),
        Pattern(
            name="dob_iso",
            regex=r"\b(?:19|20)\d{2}[/.-](?:0[1-9]|1[012])[/.-](?:0[1-9]|[12][0-9]|3[01])\b",
            score=0.90
        )
    ]
    recognizers.append(
        PatternRecognizer(
            supported_entity="DATE_OF_BIRTH",
            patterns=dob_patterns
        )
    )

    # 5. Company / Organization Recognizers
    comp_parts = []
    for c in PROSPECTUS_COMPANIES:
        esc = re.escape(c)
        if c[-1].isalnum():
            comp_parts.append(r"\b" + esc + r"\b")
        else:
            comp_parts.append(r"\b" + esc + r"(?!\w)")
    comp_regex_exact = "|".join(comp_parts)

    generic_comp_regex = r"\b[A-Z][A-Za-z0-9&\s.,-]+(?:\s+Private\s+Limited|\s+Pvt\.?\s*Ltd\.?|\s+Limited|\s+Ltd\.?|,\s*LLP|\s+LLP|\s+Inc\.?|\s+Corporation|\s+Corp\.?|\s+Bank\s+Limited|\s+Family\s+Trust|\s+Bank|\s+Associates|\s+Research)\b"
    company_patterns = [
        Pattern(name="exact_prospectus_companies", regex=comp_regex_exact, score=0.98),
        Pattern(name="generic_company_suffix", regex=generic_comp_regex, score=0.85)
    ]
    recognizers.append(
        PatternRecognizer(
            supported_entity="COMPANY",
            patterns=company_patterns
        )
    )

    # 6. Physical / Mailing Address Recognizers
    address_patterns = [
        Pattern(
            name="address_regex_full",
            regex=r"\b(?:\d{1,4}/?\d{0,4}|\bPlot No\.?|\bFlat No\.?|\bGat No\.?|\bS\.?\s*no\.?|\bSurvey No\.?|\bUnit|\bTower|\bBuilding|\bA-\d+|\bA\d+|\bC-\d+|\b\d+(?:st|nd|rd|th)\s+Floor|[A-Z0-9][A-Za-z0-9\s.\-\u2013\u2014]+?(?:House|Centre|Center|Building|Complex|Tower|Apartment|Residency|Society|Bunglow|Unit))\b[A-Za-z0-9\s,/.\-\u2013\u2014\(\)&]+?\b\d{3}\s*\d{3}\b(?:[,\s\-\u2013\u2014]+(?:Maharashtra|Madhya Pradesh|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*))?(?:[,\s\-\u2013\u2014]+India)?\.?",
            score=0.95
        ),
        Pattern(
            name="registered_office_address",
            regex=r"(?i)\b(?:Registered Office|Corporate Office|Registered and Corporate Office|Address)[:\s]+\s*([A-Za-z0-9\s,/.\-\u2013\u2014\(\)&]+?\b\d{3}\s*\d{3}\b(?:[,\s\-\u2013\u2014]+(?:Maharashtra|Madhya Pradesh|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*))?(?:[,\s\-\u2013\u2014]+India)?\.?)",
            score=0.95
        ),
        Pattern(
            name="company_prefixed_address",
            regex=r"(?i)\b[A-Za-z0-9&\s.-]+(?:Limited|LLP|Inc\.?|Corporation|Pvt\.?\s*Ltd\.?)\s*:\s*([A-Za-z0-9\s,/.\-\u2013\u2014\(\)&]+?\b\d{3}\s*\d{3}\b(?:[,\s\-\u2013\u2014]+(?:Maharashtra|Madhya Pradesh|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*))?(?:[,\s\-\u2013\u2014]+India)?\.?)",
            score=0.92
        )
    ]
    recognizers.append(
        PatternRecognizer(
            supported_entity="ADDRESS",
            patterns=address_patterns
        )
    )

    # 7. Phone Number Recognizer
    phone_patterns = [
        Pattern(
            name="phone_indian_format",
            regex=r"(?:\+\s*91|\+[\s.-]*91|\+|\b91|\b0\d{2,4})?[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{4,6}\b",
            score=0.85
        )
    ]
    recognizers.append(
        PatternRecognizer(
            supported_entity="PHONE_NUMBER",
            patterns=phone_patterns
        )
    )

    # 8. Person Name Recognizer
    name_parts = []
    for p in PROSPECTUS_NAMES:
        esc = re.escape(p)
        if p[-1].isalnum():
            name_parts.append(r"\b" + esc + r"\b")
        else:
            name_parts.append(r"\b" + esc + r"(?!\w)")
    name_regex_exact = "|".join(name_parts)

    person_patterns = [
        Pattern(name="exact_prospectus_names", regex=name_regex_exact, score=0.98),
        Pattern(
            name="person_title_pattern",
            regex=r"\b(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?|Shri\.?)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b",
            score=0.85
        )
    ]
    recognizers.append(
        PatternRecognizer(
            supported_entity="PERSON",
            patterns=person_patterns
        )
    )

    return recognizers


def register_all_custom_recognizers(analyzer):
    """Registers all custom recognizers into the given Presidio AnalyzerEngine."""
    for recognizer in get_custom_recognizers():
        analyzer.registry.add_recognizer(recognizer)
    return analyzer
