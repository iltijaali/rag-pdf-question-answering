# ==================================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# ==================================================

import os
import json

# Load PDF files
from langchain_community.document_loaders import PyPDFLoader

# Create custom documents from JSON
from langchain_core.documents import Document

# Semantic Chunking
from langchain_experimental.text_splitter import SemanticChunker

# Chroma Vector Database
from langchain_chroma import Chroma

# Embedding Model
from langchain_huggingface import HuggingFaceEmbeddings

# Load HF Token
import config


# ==================================================
# STEP 2: LOAD ALL PDF & JSON FILES
# ==================================================

print("Loading PDFs and JSON Files...")

data_folder = "data"

# Store all documents
documents = []

# Loop through all files inside data folder
for file in os.listdir(data_folder):

    file_path = os.path.join(data_folder, file)

    # ==================================================
    # LOAD PDF FILES
    # ==================================================
    if file.endswith(".pdf"):

        print(f"Loading PDF: {file}")

        loader = PyPDFLoader(file_path)

        docs = loader.load()

        # Add source filename
        for doc in docs:
            doc.metadata["source_file"] = file

        documents.extend(docs)

    # ==================================================
    # LOAD JSON FILES
    # ==================================================
    elif file.endswith(".json"):

        print(f"Loading JSON: {file}")

        try:

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Convert JSON into readable text
            text = json.dumps(data, indent=2)

            # Create LangChain Document
            doc = Document(
                page_content=text,
                metadata={
                    "source_file": file,
                    "file_type": "json"
                }
            )

            documents.append(doc)

        except Exception as e:
            print(f"Error loading {file}: {e}")

print(f"\nTotal Documents Loaded: {len(documents)}")


# ==================================================
# STEP 3: LOAD EMBEDDING MODEL
# ==================================================

print("\nLoading Embedding Model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding Model Loaded Successfully!")


# ==================================================
# STEP 4: CREATE SEMANTIC CHUNKS
# ==================================================

print("\nCreating Semantic Chunks...")

text_splitter = SemanticChunker(
    embeddings
)

chunks = text_splitter.split_documents(documents)

print(f"Total Semantic Chunks Created: {len(chunks)}")


# ==================================================
# STEP 5: CHECK EXISTING DATABASE
# ==================================================

if os.path.exists("db"):

    print("\nOld ChromaDB found.")
    print("Existing data will be updated/overwritten.")


# ==================================================
# STEP 6: CREATE CHROMADB VECTOR DATABASE
# ==================================================

print("\nCreating ChromaDB Vector Database...")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="db"
)

print("\nVector Database Created Successfully!")

print(f"Stored {len(chunks)} Chunks in ChromaDB")


# ==================================================
# STEP 7: SHOW SAMPLE CHUNKS
# ==================================================

print("\nSample Chunks Preview")

for i, chunk in enumerate(chunks[:5]):

    print("\n" + "=" * 60)

    print(f"Chunk #{i+1}")

    print(f"Source File: {chunk.metadata.get('source_file')}")

    print(chunk.page_content[:300])

    print("\n" + "=" * 60)


# ==================================================
# STEP 8: SUCCESS MESSAGE
# ==================================================

print("\n========================================")
print("Data Ingestion Completed Successfully!")
print("PDF Files Loaded")
print("JSON Files Loaded")
print("Semantic Chunking Applied")
print("ChromaDB Created Successfully!")
print("========================================")
