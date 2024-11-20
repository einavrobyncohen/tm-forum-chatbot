import json

input_file = "extracted_text.json"
with open(input_file, "r", encoding="utf-8") as f:
    #Loading the JSON file as a python dict
    pdf_data = json.load(f)

def clean_text(text):
    text = " ".join(text.split())
    #removing common headers/footers.
    for pattern in ["page", "TM Forum"]:
        text = text.replace(pattern, "")
    return text 

clean_data = {}
for file_name, text in pdf_data.items():
    clean_data[file_name] = clean_text(text)

output_file = "cleaned_text.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(clean_data, f, ensure_ascii=False, indent=4)

print(f"Cleaned text saved to {output_file}")