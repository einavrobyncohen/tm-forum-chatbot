import json

input_file = "cleaned_text.json"
with open(input_file, "r", encoding="utf-8") as f:
    cleaned_data = json.load(f)

def chunk_text(text, chunk_size = 500):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

chunked_data = {}

for file_name, text in cleaned_data.items():
    chunked_data[file_name] = chunk_text(text, chunk_size=500)

output_file = "chunked_text.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(chunked_data, f, ensure_ascii=False, indent=4)

print(f"Chunked text saved to {output_file}")