import json
import os

def load_sensitive_topics(file_path):
    """
    Load a user-defined JSON file of sensitive categories and phrases.

    Expected JSON structure:
    {
      "Category1": ["trigger phrase1", "trigger phrase2"],
      ...
    }

    Returns:
        dict: category -> list of trigger phrases
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Topic file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {file_path}: {e}")
    
    if not isinstance(data, dict):
        raise ValueError("Sensitive topic file must be a JSON object with categories as keys.")
    
    for category, terms in data.items():
        if not isinstance(terms, list):
            raise ValueError(f"Each category must map to a list of strings: {category}")
        if not all(isinstance(term, str) for term in terms):
            raise ValueError(f"All entries under category '{category}' must be strings.")

    return data

