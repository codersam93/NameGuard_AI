import zipfile
import os

zip_path = "NameGuard_AI_v2-main.zip"
extract_path = "temp_unzip"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print(f"Extracted to {extract_path}")
