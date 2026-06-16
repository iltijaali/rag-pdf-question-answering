# ==========================================
# VIEW CHROMADB DATA
# ==========================================

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to ChromaDB
db = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)

# Access underlying collection
collection = db._collection

# Get all data
data = collection.get()

print(f"\nTotal Chunks: {len(data['documents'])}")

for i in range(len(data["documents"])):

    print("\n" + "=" * 60)

    print(f"Chunk #{i+1}")

    print("\nSource:")
    print(data["metadatas"][i])

    print("\nContent:")
    print(data["documents"][i][:500])

    print("\nVector ID:")
    print(data["ids"][i])
