# Semantic Chunking RAG Project

This project is a simple Retrieval-Augmented Generation style document search system built with LangChain, Hugging Face embeddings, semantic chunking, and ChromaDB.

The app loads PDF and JSON files from the `data/` folder, converts them into semantic chunks, stores those chunks in a local Chroma vector database, and lets the user ask questions from the indexed documents.

## Project Goal

The main goal of this project is to test whether semantic chunking is working correctly for document retrieval.

It is designed to verify:

- Relevant chunks are retrieved for document-based questions.
- Similar documents are not confused with each other.
- Questions outside the documents return a clear not-found message.
- Missing fields, such as a CEO or price not present in the PDF, do not produce misleading answers.
- Chunk quality can be inspected manually using `view_db.py`.

## Project Structure

```text
RAG1/
|-- data/
|   |-- Devsinc.pdf
|   |-- OWASP top 10 vulnerabilities.pdf
|   |-- Skill Pass.pdf
|   |-- Systems Limited.pdf
|   `-- vertxSoft.pdf
|-- db/
|   `-- Local ChromaDB vector database
|-- ingest.py
|-- query.py
|-- view_db.py
|-- config.py
|-- requirements.txt
|-- .env.example
|-- .gitignore
`-- SEMANTIC_CHUNKING_TEST_CASES.md
```

## Main Files

### `ingest.py`

This script loads all supported files from the `data/` folder.

It performs these steps:

1. Loads PDF files using `PyPDFLoader`.
2. Loads JSON files if any are present.
3. Creates embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
4. Applies LangChain `SemanticChunker`.
5. Stores chunks in local ChromaDB inside the `db/` folder.
6. Prints sample chunks for quick checking.

### `query.py`

This script asks the user for a question and searches ChromaDB for the most relevant chunk.

It includes a not-found check:

- If the question is unrelated to the documents, it prints:

```text
Data you search is not found in documents.
```

- If the user asks for a field that is not present, such as CEO, price, revenue, percentage, or share price, it also returns the same not-found message.

### `view_db.py`

This script shows all stored ChromaDB chunks.

Use it to inspect:

- Total chunks
- Chunk source metadata
- Chunk content preview
- Vector IDs

### `SEMANTIC_CHUNKING_TEST_CASES.md`

This file contains manual test cases for checking retrieval accuracy, chunk quality, unsupported questions, cross-page boundaries, and document disambiguation.

## Data Sources

The current `data/` folder contains these PDFs:

- `Devsinc.pdf`
- `Systems Limited.pdf`
- `vertxSoft.pdf`
- `Skill Pass.pdf`
- `OWASP top 10 vulnerabilities.pdf`

These documents are used to test company-profile retrieval, SkillPass platform questions, and OWASP security-topic questions.

## Setup

### 1. Create Virtual Environment

```powershell
python -m venv venv
```

### 2. Activate Virtual Environment

```powershell
.\venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create `.env` File

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Then add your Hugging Face token if needed:

```text
HF_TOKEN=your_token_here
```

The current embedding model may work without a token in many environments, but the project supports loading one through `config.py`.

## How to Run

### Step 1: Ingest Documents

Run:

```powershell
python ingest.py
```

This creates or updates the local ChromaDB database in the `db/` folder.

### Step 2: Ask Questions

Run:

```powershell
python query.py
```

Then enter a question.

Example:

```text
Who is the CEO of Systems Limited?
```

Expected result: the retrieved chunk should contain:

```text
CEO: Muhammad Asif Peer
```

### Step 3: Inspect Stored Chunks

Run:

```powershell
python view_db.py
```

This helps verify whether semantic chunks are meaningful and whether the source metadata is correct.

## Example Questions

Valid document questions:

```text
Who founded Devsinc?
```

```text
What is the stock ticker of Systems Limited?
```

```text
What is SkillPass used for?
```

```text
What is Broken Access Control in OWASP?
```

Unsupported or missing-data questions:

```text
Who is the CEO of VertXSoft?
```

```text
What is the monthly price of SkillPass?
```

```text
What is the capital of France?
```

For unsupported questions, the app should print:

```text
Data you search is not found in documents.
```

## Testing Semantic Chunking

Use:

```text
SEMANTIC_CHUNKING_TEST_CASES.md
```

Recommended testing flow:

1. Run `python ingest.py`.
2. Run `python query.py`.
3. Ask questions from the test cases file.
4. Check whether the returned chunk contains the expected source and facts.
5. Run `python view_db.py` to inspect chunk quality manually.

## Current Query Behavior

The query script currently:

- Searches the vector database using similarity search with scores.
- Retrieves multiple candidate chunks internally.
- Prints only the best chunk.
- Uses a distance threshold to reject weak matches.
- Checks common missing fields before printing a chunk.

Important settings in `query.py`:

```python
NOT_FOUND_SCORE = 1.45
CHUNKS_TO_PRINT = 1
```

If the system rejects too many valid questions, increase `NOT_FOUND_SCORE`.

If the system returns unrelated chunks, decrease `NOT_FOUND_SCORE`.

## Limitations

- This project retrieves chunks; it does not generate polished natural-language answers using an LLM.
- Some answers may require reading the returned chunk manually.
- Semantic search can still retrieve similar but incorrect chunks when documents share many terms.
- The not-found threshold may need adjustment after changing documents or chunking settings.
- Re-running ingestion may add/update Chroma data depending on the existing database state.

## Ignored Files

The `.gitignore` file excludes:

```text
venv/
db/
.env
__pycache__/
*.pyc
.vscode/
```

This prevents virtual environments, local databases, secrets, cache files, and editor settings from being committed.

## Requirements

Main packages used:

- LangChain
- LangChain Community
- LangChain Experimental
- ChromaDB
- Hugging Face embeddings
- Sentence Transformers
- PyPDF
- Python Dotenv

Install all packages with:

```powershell
pip install -r requirements.txt
```

## Future Improvements

Possible next steps:

- Add an LLM answer-generation step after retrieval.
- Clear or recreate the ChromaDB collection before each ingestion.
- Store page numbers and chunk IDs more clearly.
- Add automated tests for the questions in `SEMANTIC_CHUNKING_TEST_CASES.md`.
- Add reranking to improve results for similar company profiles.
- Add source citations in the final response.

## Summary

This project is useful for learning and testing semantic chunking in a local RAG pipeline. It helps compare retrieval quality across multiple similar PDFs and checks whether unsupported questions are correctly rejected instead of returning unrelated document text.
