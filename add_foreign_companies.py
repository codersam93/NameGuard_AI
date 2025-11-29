import pandas as pd
from datetime import datetime, timezone
import uuid

# Helper functions from scoring.py
def normalize_name(raw: str) -> str:
    base = raw.strip().lower()
    suffixes = [
        "private limited", "pvt ltd", "limited", "ltd", 
        "opc private limited", "llp", "producer company limited"
    ]
    for suf in suffixes:
        if base.endswith(suf):
            base = base[: -len(suf)].strip()
            break
    return " ".join(base.split())

def simple_phonetic_key(raw: str) -> str:
    s = normalize_name(raw)
    repl = [
        ("ph", "f"), ("bh", "b"), ("kh", "k"), ("gh", "g"), 
        ("ch", "c"), ("sh", "s"), ("ss", "s"), ("aa", "a"), 
        ("ee", "i"), ("oo", "u")
    ]
    for a, b in repl:
        s = s.replace(a, b)
    return "".join(c for c in s if c.isalnum())

# List of US companies operating in India
companies = [
    "Google India Private Limited",
    "Microsoft Corporation (India) Private Limited",
    "Amazon Development Centre (India) Private Limited",
    "Apple India Private Limited",
    "Facebook India Online Services Private Limited",
    "IBM India Private Limited",
    "Oracle India Private Limited",
    "Cisco Systems (India) Private Limited",
    "Intel Technology India Private Limited",
    "Hewlett-Packard India Sales Private Limited",
    "Dell International Services India Private Limited",
    "Netflix Entertainment Services India LLP",
    "Uber India Systems Private Limited",
    "Walmart India Private Limited",
    "Coca-Cola India Private Limited",
    "PepsiCo India Holdings Private Limited",
    "General Electric Company",
    "JPMorgan Chase Bank",
    "Goldman Sachs (India) Securities Private Limited",
    "Morgan Stanley India Company Private Limited",
    "Adobe Systems India Private Limited",
    "Salesforce.com India Private Limited",
    "VMware Software India Private Limited",
    "Qualcomm India Private Limited",
    "NVIDIA Graphics Private Limited",
    "American Express (India) Private Limited",
    "Citibank N.A.",
    "Bank of America",
    "Ford Motor Private Limited",
    "General Motors India Private Limited",
    "Boeing India Private Limited",
    "Lockheed Martin India Private Limited",
    "Pfizer Limited",
    "Johnson & Johnson Private Limited",
    "Procter & Gamble Hygiene and Health Care Limited",
    "McDonald's India Private Limited",
    "Starbucks Coffee",
    "Nike India Private Limited",
    "Visa Consolidated Support Services (India) Private Limited",
    "Mastercard India Services Private Limited"
]

new_rows = []
now_iso = datetime.now(timezone.utc).isoformat()

for name in companies:
    normalized = normalize_name(name)
    key = simple_phonetic_key(name)
    
    row = {
        'name_original': name,
        'name_normalized': normalized,
        'phonetic_key': key,
        'language_tags': 'en',
        'decision': 'accepted',
        'reason_codes': '[]',
        'mca_officer_id': 'system_import_us_companies',
        'score_at_time': 0.98,
        'decision_timestamp': now_iso
    }
    new_rows.append(row)

# Load existing data
file_path = '/app/data/historical_name_decisions.xlsx'
try:
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} existing records.")
except Exception as e:
    print(f"Error loading file: {e}")
    # Create empty df if file doesn't exist or error
    df = pd.DataFrame(columns=['name_original', 'name_normalized', 'phonetic_key', 'language_tags',
                               'decision', 'reason_codes', 'mca_officer_id', 'score_at_time',
                               'decision_timestamp'])

# Append new data
new_df = pd.DataFrame(new_rows)
combined_df = pd.concat([df, new_df], ignore_index=True)

# Save back
combined_df.to_csv(file_path, index=False)
print(f"Added {len(new_rows)} new records. Total records: {len(combined_df)}")
