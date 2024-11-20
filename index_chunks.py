import json
import faiss  # For indexing and similarity search
from sentence_transformers import SentenceTransformer

# 1. Load the chunked text data
input_file = "chunked_text.json"
with open(input_file, "r", encoding="utf-8") as f:
    chunked_data = json.load(f)

# 2. Prepare text chunks and metadata
texts = []  # List to hold all text chunks
metadata = []  # List to hold metadata (e.g., file names and chunk indices)

for file_name, chunks in chunked_data.items():
    for idx, chunk in enumerate(chunks):
        texts.append(chunk)  # Add the text chunk
        metadata.append({"file": file_name, "chunk_index": idx})  # Store metadata

# 3. Convert text to embeddings using SentenceTransformer
print("Generating embeddings...")
model = SentenceTransformer('all-MiniLM-L6-v2')  # Pretrained embedding model
embeddings = model.encode(texts, show_progress_bar=True, batch_size=16)

# 4. Create a FAISS index
dimension = embeddings.shape[1]  # The embedding size
index = faiss.IndexFlatL2(dimension)  # Create a flat L2 index
index.add(embeddings)  # Add the embeddings to the index
print(f"Indexed {len(texts)} text chunks.")

# 5. Save the FAISS index and metadata
faiss.write_index(index, "chunk_index.faiss")  # Save the FAISS index
with open("chunk_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=4)  # Save metadata

print("FAISS index and metadata saved.")
