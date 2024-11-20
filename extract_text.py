import os
import pdfplumber 
import json

pdf_folder = "TM Forum Guides"
output_file = "extracted_text.json"
pdf_data = {}

for file_name in os.listdir(pdf_folder):
    if file_name.endswith(".pdf"):
        file_path = os.path.join(pdf_folder, file_name)

        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            pdf_data[file_name] = text

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(pdf_data, f, ensure_ascii=False, indent=4)

print(f"Text extracted and saved to {output_file}")
