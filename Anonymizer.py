# Anonymizer.py
import spacy
from docx import Document

def create_nlp_pipeline():
    nlp = spacy.load("en_core_web_sm")
    ruler = nlp.add_pipe("entity_ruler", before="ner")

    patterns = [
        {
            "label": "PHONE_NUMBER",
            "pattern": [
                {"TEXT": {"REGEX": r"^\+?\d{1,3}$"}, "OP": "?"},
                {"TEXT": {"REGEX": r"^[-.\s]+$"}, "OP": "?"},
                {"TEXT": {"REGEX": r"^\d{3,4}$"}},
                {"TEXT": {"REGEX": r"^[-.\s]+$"}, "OP": "?"},
                {"TEXT": {"REGEX": r"^\d{3}$"}},
                {"TEXT": {"REGEX": r"^[-.\s]+$"}, "OP": "?"},
                {"TEXT": {"REGEX": r"^\d{3,4}$"}}
            ]
        },
        {
            "label": "POST_ADDRESS_EU",
            "pattern": [
                {"TEXT": {"REGEX": r"^\d{4,5}$"}},  # Postal code: 4 or 5 digits
                {"TEXT": {"REGEX": r"^\s*$"}, "OP": "?"},  # Optional whitespace (if needed)
                {"TEXT": {"REGEX": r"^[A-Za-zÀ-ÖØ-öø-ÿ\s\-]+$"}}
                # City name: letters (including accented), spaces, hyphens
            ]
        },
        {
            "label": "SALARY_EU_NOK_USD",
            "pattern": [
                {"TEXT": {"REGEX": r"^\d{1,3}(,\d{3})*$"}},  # Salary amount formatted with commas (e.g., 1,234)
                {"TEXT": {"REGEX": r"^(€|EUR|NOK|\$|USD)$"}}  # Currency: Euro symbol/abbr, NOK, Dollar symbol, or USD
            ]
        },
        {
            "label": "DATE",
            "pattern": [
                {"TEXT": {"REGEX": r"^\d{1,2}/\d{1,2}/\d{4}$"}}
            ]
        },
        {
            "label": "ACCOUNT_NUMBER",
            "pattern": [{"TEXT": {"REGEX": r"^\d{6,12}$"}}]
        },
        {
            "label": "CREDIT_CARD",
            "pattern": [
                {"TEXT": {"REGEX": r"^\d{4}$"}},
                {"TEXT": {"REGEX": r"^[-.\s]+$"}, "OP": "?"},
                {"TEXT": {"REGEX": r"^\d{4}$"}},
                {"TEXT": {"REGEX": r"^[-.\s]+$"}, "OP": "?"},
                {"TEXT": {"REGEX": r"^\d{4}$"}},
                {"TEXT": {"REGEX": r"^[-.\s]+$"}, "OP": "?"},
                {"TEXT": {"REGEX": r"^\d{4}$"}}
            ]
        },
        {
            "label": "EMAIL",
            "pattern": [{"TEXT": {"REGEX": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"}}]
        },
        {
            "label": "ID_NUMBER",
            "pattern": [{"TEXT": {"REGEX": r"^\d{11}$"}}]
        },
        {
            "label": "COORDINATES",
            "pattern": [
                {"TEXT": {"REGEX": r"^\($"}},
                {"TEXT": {"REGEX": r"^-?\d+(\.\d+)?$"}},
                {"TEXT": {"REGEX": r"^,$"}},
                {"TEXT": {"REGEX": r"^-?\d+(\.\d+)?$"}},
                {"TEXT": {"REGEX": r"^\)$"}}
            ]
        },
        {
            "label": "ADDRESS",
            "pattern": [
                {"TEXT": {"REGEX": r"^\d+$"}},
                {"TEXT": {"REGEX": r"^[A-Za-z]+$"}},
                {"TEXT": {"REGEX": r"^(Street|St|Road|Rd|Ave|Avenue|Blvd|Boulevard|Lane|Ln)$"}},
                {"TEXT": {"REGEX": r"^,$"}, "OP": "?"},
                {"TEXT": {"REGEX": r"^[A-Za-z]+$"}}
            ]
        }
    ]

    ruler.add_patterns(patterns)
    return nlp

def anonymize_text(text, nlp, allowed_labels):
    doc = nlp(text)
    new_text = []
    last_end = 0
    for ent in doc.ents:
        if ent.label_ in allowed_labels:
            new_text.append(text[last_end:ent.start_char])
            new_text.append(f"[{ent.label_}]")
            last_end = ent.end_char
    new_text.append(text[last_end:])
    return "".join(new_text)

def anonymize_docx(input_path, output_path, nlp, allowed_labels):
    doc = Document(input_path)
    for paragraph in doc.paragraphs:
        original_text = paragraph.text
        anonymized = anonymize_text(original_text, nlp, allowed_labels)
        paragraph.text = anonymized
    doc.save(output_path)

def run_anonymization(input_path, output_path):
    nlp = create_nlp_pipeline()
    allowed_labels = {
        "PERSON", "GPE", "ORG", "DATE", "MONEY", "CARDINAL",
    "NORP", "LOC", "EMAIL", "PHONE_NUMBER", "CREDIT_CARD",
    "ACCOUNT_NUMBER", "ID_NUMBER", "COORDINATES", "ADDRESS",
    "POST_ADDRESS_EU", "SALARY_EU_NOK_USD"
    }
    anonymize_docx(input_path, output_path, nlp, allowed_labels)
    return output_path




#%%
