from flask import Flask, request, render_template
import faiss
import json
from sentence_transformers import SentenceTransformer

# Initialize the Flask app
app = Flask(__name__)

# Load FAISS index and metadata
index = faiss.read_index("chunk_index.faiss")
with open("chunk_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route("/", methods=["GET", "POST"])
def chatbot():
    results = []
    if request.method == "POST":
        query = request.form["query"]

        # Encode the query and search the FAISS index
        query_embedding = model.encode([query])
        k = 3  # Number of top results to retrieve
        distances, indices = index.search(query_embedding, k)

        # Retrieve metadata and chunk content for the top results
        for i, idx in enumerate(indices[0]):
            file_name = metadata[idx]["file"]
            chunk_index = metadata[idx]["chunk_index"]

            # Load the chunked text
            with open("chunked_text.json", "r", encoding="utf-8") as f:
                chunked_data = json.load(f)
            chunk_content = chunked_data[file_name][chunk_index]

            # Format the result for the UI
            result = {
                "file": file_name,
                "chunk_index": chunk_index,
                "distance": f"{distances[0][i]:.4f}",
                "content": chunk_content,
            }
            results.append(result)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
